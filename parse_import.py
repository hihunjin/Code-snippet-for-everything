import os
import ast
from glob import glob
from pathlib import Path
from typing import List, Tuple


def parse_compile_list(
    modules: List[str],
    extra_sys_paths: List[str] = None,
    exclude: List[str] = None,
) -> Tuple[List[str]]:
    """returns python files to be built by recursively parsing `import` phrases.

    Reference:
        https://github.com/andrewp-as-is/list-imports.py/blob/master/list_imports/__init__.py

    Note:
        file/dir의 존재 유무를 isfile/isdir 함수에서 glob의 string comapre로 변경한 이유.

        이슈
            window에서는 filename의 대소문자를 구분하지 않음,
                "A.py", "a.Py", "a.PY"가 모두 같은 file.
            os.path.isfile/isdir 함수 또한 대소문자를 구분하지 않음,
                "A"가 존재할 때 isfile("a")을 호출시 True return.
            따라서 폴더 내부가 다음과 같이 되어있고, import A를 했다면
            ├── A
            │   └── __init__.py
            └── a.py
            linux의 경우는 A.py가 없기 때문에, A directory를 잘 찾지만,
            window의 경우에는 isfile(A.py)가 True이기 때문에 logic에 문제가 발생.

        해결 방법
            glob로 모든 file name, directory name을 가져온 뒤, string compare 진행.

        unresolved issue
            glob가 모든 파일 리스트를 읽어오기 때문에, 폴더 내에 파일이 많은 경우 속도가 느려지는 이슈.
    """
    compile_list = []
    all_existing_files = glob("**", recursive=True)
    all_existing_files = [
        f
        for f in all_existing_files
        if all(ex not in f for ex in (exclude or []))
    ]
    all_existing_directories = glob("**" + os.sep, recursive=True)
    all_existing_directories = [
        f
        for f in all_existing_directories
        if all(ex not in f for ex in (exclude or []))
    ]

    def _parse_compile_list(module: str) -> None:
        import_list = get_import_module_list(module)

        # recursively update compile list
        for imp_temp in import_list:
            import_path = imp_temp.replace(".", os.path.sep)
            import_paths = [sys_path / import_path for sys_path in extra_sys_paths] if extra_sys_paths else [import_path]

            for _imp in import_paths:
                _imp = str(_imp)
                if _imp + ".py" in all_existing_files and _imp not in compile_list:
                    compile_list.append(_imp)
                    _parse_compile_list(_imp)

                elif (
                    _imp + os.sep in all_existing_directories
                    and _imp + ".__init__" not in compile_list
                ):
                    compile_list.append(_imp + ".__init__")
                    _parse_compile_list(_imp + ".__init__")

    for module in modules:
        _parse_compile_list(module)

    compile_list = [f + ".py" if not f.endswith(".py") else f for f in compile_list]
    return sorted(list(set(compile_list))), sorted(list(set(all_existing_files) - set(compile_list)))


def get_import_module_list(module: str) -> List[str]:
    """Get importing module list from single python file"""
    path = module.replace(".", os.path.sep)
    path = path[:-3] + ".py" if path.endswith(os.path.sep + "py") else path + ".py"
    assert os.path.isfile(path), f"should be file path: {path}"

    directory = os.path.dirname(path)
    with open(path, encoding="utf-8") as f:
        code = f.read()
    tree = ast.parse(code)

    # Get importing module list
    import_list = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            # style of [import A]
            for subnode in node.names:
                import_list.append(subnode.name)
        if isinstance(node, ast.ImportFrom):
            if node.module is None:
                # style of [from .. import A]
                import_list.extend(["." * node.level + n.name for n in node.names])
            else:
                # style of [from A import B] or [from ..A import B]
                # add "A" or "..A"
                import_list.append("." * node.level + node.module)
                # add "A.B" or "..A.B"
                import_list.extend(["." * node.level + node.module + "." + n.name for n in node.names])

    # Interpret dot-representation
    for idx, imp in enumerate(import_list):
        if imp[0] != ".":
            continue
        dot_directory = directory
        while imp[1] == ".":
            dot_directory = os.path.dirname(dot_directory)
            imp = imp[1:]
        import_list[idx] = dot_directory.replace(os.path.sep, ".") + imp

    return import_list


if __name__ == "__main__":
    base = Path(".").parent.parent
    extra_paths = [
        base,
        base / "src",
        base / "src" / "ixi_rag_july_demo",
        base / "chunker" / "src",
        base / "doc_recognition" / "src",
    ]
    exclude = ["__pycache__", ".cu", ".pyc", ".so", ".pyd", ".ipynb_checkpoints", "DCNv2_latest", "tests/"]
    used, unused = parse_compile_list(
        ["src.ixi_rag_july_demo.run_end_to_end.py"],
        extra_sys_paths=extra_paths,
        exclude=exclude,
    )
    print("Used files(py):")
    print("\n".join(used))
    print("\nUnused files(py):")
    print("\n".join(unused))
