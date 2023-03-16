# 아래 loop.sh파일과 같은 bat파일
# export DN="
# d1
# d2
# d3
# d4
# "
# export NT="
# n1
# n2
# n3
# "

# for dataset in $DN
# do
#     for network_t in $NT
#     do
#         python folder/run.py -d $dataset --logdir ../$dataset/$network_t -m $network_t
#     done
# done

$env:DN = @("d1", "d2", "d3", "d4")
$env:NT = @("n1", "n2", "n3")

for %%d in (%DN%) do (
    for %%t in (%NT%) do (
        python folder/run.py -d %%d --logdir ../%%d/%%t -m %%t
    )
)
