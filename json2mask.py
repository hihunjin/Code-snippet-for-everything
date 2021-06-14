'''
mkdir mask
python json2mask.py /path/to/sample_label.json mask
'''


import os
import sys
import json
import numpy
from PIL import Image, ImageDraw

# Opening JSON file
f = open(sys.argv[1],)
data = json.load(f)
f.close()
# print(data)
# annotations [{'file_name': 'img01.jpg', 'polygon1': [{'x': 241.7037811279297, 'y': 82.57260131835938}, {'x': 242.55335998535156, 'y': 95.31620788574219}, {'x': 243.82772827148438, 'y': 101.9004135131836}, {'x': 228.96018981933594, 'y': 113.15726470947266}, {'x': 221.73880004882812, 'y': 124.20172882080078}, {'x': 219.82725524902344, 'y': 133.5470428466797}, {'x': 215.1546173095703, 'y': 151.38809204101562}, {'x': 211.33151245117188, 'y': 159.2466583251953}, {'x': 207.72084045410156, 'y': 160.94580078125}, {'x': 196.67637634277344, 'y': 142.04278564453125}, {'x': 189.87977600097656, 'y': 137.79490661621094}, {'x': 187.54344177246094, 'y': 136.94532775878906}, {'x': 186.6938934326172, 'y': 137.58251953125}, {'x': 183.08319091796875, 'y': 139.2816619873047}, {'x': 176.9237823486328, 'y': 136.94532775878906}, {'x': 170.33958435058594, 'y': 138.4320831298828}, {'x': 165.8793182373047, 'y': 139.2816619873047}, {'x': 158.87033081054688, 'y': 122.92736053466797}, {'x': 154.83485412597656, 'y': 91.91791534423828}, {'x': 154.1976776123047, 'y': 78.11233520507812}, {'x': 160.1446990966797, 'y': 58.14734649658203}, {'x': 163.11819458007812, 'y': 46.040924072265625}, {'x': 180.5344696044922, 'y': 32.23534393310547}, {'x': 189.66738891601562, 'y': 22.677637100219727}, {'x': 201.1366424560547, 'y': 17.58019256591797}, {'x': 213.03067016601562, 'y': 13.757109642028809}, {'x': 226.4114532470703, 'y': 9.721633911132812}, {'x': 233.20806884765625, 'y': 8.872058868408203}, {'x': 244.0401153564453, 'y': 8.447272300720215}, {'x': 251.898681640625, 'y': 8.447272300720215}, {'x': 259.54486083984375, 'y': 9.296846389770508}, {'x': 270.58929443359375, 'y': 11.420782089233398}, {'x': 278.2354736328125, 'y': 13.544716835021973}, {'x': 285.45684814453125, 'y': 15.243864059448242}, {'x': 295.4393310546875, 'y': 17.792587280273438}, {'x': 302.2359313964844, 'y': 19.916521072387695}, {'x': 308.60772705078125, 'y': 22.890029907226562}, {'x': 316.46630859375, 'y': 26.713111877441406}, {'x': 322.8381042480469, 'y': 32.66012954711914}, {'x': 333.457763671875, 'y': 43.27980422973633}, {'x': 335.7940979003906, 'y': 45.828529357910156}, {'x': 340.89154052734375, 'y': 50.07640075683594}, {'x': 346.8385925292969, 'y': 56.23580551147461}, {'x': 352.3608093261719, 'y': 65.58112335205078}, {'x': 355.9714660644531, 'y': 75.56361389160156}, {'x': 357.2458801269531, 'y': 81.9354248046875}, {'x': 357.2458801269531, 'y': 102.53758239746094}, {'x': 353.8475646972656, 'y': 105.08631134033203}, {'x': 351.7236328125, 'y': 102.32520294189453}, {'x': 347.05096435546875, 'y': 79.59909057617188}, {'x': 344.50225830078125, 'y': 73.43968200683594}, {'x': 339.6171875, 'y': 74.07686614990234}, {'x': 336.2189025878906, 'y': 74.50164794921875}, {'x': 333.457763671875, 'y': 74.71404266357422}, {'x': 334.094970703125, 'y': 67.7050552368164}, {'x': 333.457763671875, 'y': 66.6430892944336}, {'x': 324.7496337890625, 'y': 68.97942352294922}, {'x': 319.2274169921875, 'y': 71.10334777832031}, {'x': 310.519287109375, 'y': 73.6520767211914}, {'x': 300.11199951171875, 'y': 77.05036926269531}, {'x': 305.2094421386719, 'y': 70.25377655029297}, {'x': 301.1739501953125, 'y': 69.40420532226562}, {'x': 295.8641357421875, 'y': 69.40420532226562}, {'x': 284.3948974609375, 'y': 70.89096069335938}, {'x': 276.96112060546875, 'y': 70.6785659790039}, {'x': 265.27947998046875, 'y': 71.74053192138672}, {'x': 248.28799438476562, 'y': 72.37771606445312}, {'x': 242.12857055664062, 'y': 74.92643737792969}]}, {'file_name': 'img02.jpg', 'polygon1': [{'x': 153.4588623046875, 'y': 100.61593627929688}, {'x': 152.4029541015625, 'y': 91.81669616699219}, {'x': 161.2021942138672, 'y': 68.23471069335938}, {'x': 174.9290313720703, 'y': 52.39606475830078}, {'x': 181.96841430664062, 'y': 50.6362190246582}, {'x': 185.13613891601562, 'y': 47.820457458496094}, {'x': 197.10313415527344, 'y': 43.244850158691406}, {'x': 216.4614715576172, 'y': 40.781063079833984}, {'x': 219.2772216796875, 'y': 22.830596923828125}, {'x': 225.96466064453125, 'y': 13.327411651611328}, {'x': 247.0828399658203, 'y': 8.399833679199219}, {'x': 260.1057434082031, 'y': 10.511653900146484}, {'x': 269.2569580078125, 'y': 11.567562103271484}, {'x': 274.5364990234375, 'y': 19.31089973449707}, {'x': 274.8884582519531, 'y': 23.53453826904297}, {'x': 291.78302001953125, 'y': 27.758176803588867}, {'x': 305.50982666015625, 'y': 35.14954376220703}, {'x': 320.99652099609375, 'y': 43.94879150390625}, {'x': 335.4272766113281, 'y': 58.37955093383789}, {'x': 341.7627258300781, 'y': 70.34652709960938}, {'x': 347.04229736328125, 'y': 78.79380798339844}, {'x': 356.8974304199219, 'y': 83.72138214111328}, {'x': 362.52899169921875, 'y': 92.5206298828125}, {'x': 361.4730529785156, 'y': 107.65532684326172}, {'x': 364.288818359375, 'y': 117.15852355957031}, {'x': 363.93682861328125, 'y': 125.25382232666016}, {'x': 365.6966857910156, 'y': 135.46095275878906}, {'x': 366.400634765625, 'y': 145.66807556152344}, {'x': 369.2164001464844, 'y': 153.7633819580078}, {'x': 371.68017578125, 'y': 159.7468719482422}, {'x': 380.12744140625, 'y': 163.61854553222656}, {'x': 385.75897216796875, 'y': 172.76976013183594}, {'x': 387.1668395996094, 'y': 187.552490234375}, {'x': 383.295166015625, 'y': 194.94386291503906}, {'x': 383.9991455078125, 'y': 203.03916931152344}, {'x': 378.7195739746094, 'y': 216.06204223632812}, {'x': 368.512451171875, 'y': 222.0455322265625}, {'x': 365.6966857910156, 'y': 224.5093231201172}, {'x': 364.288818359375, 'y': 233.66055297851562}, {'x': 366.04864501953125, 'y': 236.1243438720703}, {'x': 370.27227783203125, 'y': 243.16372680664062}, {'x': 369.92034912109375, 'y': 250.203125}, {'x': 364.6407775878906, 'y': 260.4102478027344}, {'x': 358.65728759765625, 'y': 262.5220642089844}, {'x': 362.177001953125, 'y': 248.4432830810547}, {'x': 360.065185546875, 'y': 243.16372680664062}, {'x': 355.8415222167969, 'y': 245.9794921875}, {'x': 353.3777160644531, 'y': 255.83465576171875}, {'x': 354.0816650390625, 'y': 262.17010498046875}, {'x': 366.04864501953125, 'y': 265.33782958984375}, {'x': 371.68017578125, 'y': 272.0252685546875}, {'x': 360.76910400390625, 'y': 278.71270751953125}, {'x': 355.8415222167969, 'y': 282.5843811035156}, {'x': 349.8580627441406, 'y': 290.6796569824219}, {'x': 351.2658996582031, 'y': 281.1764831542969}, {'x': 346.6903076171875, 'y': 284.6961669921875}, {'x': 344.2265319824219, 'y': 301.9427185058594}, {'x': 339.2989501953125, 'y': 308.630126953125}, {'x': 337.1871337890625, 'y': 309.68603515625}, {'x': 336.1312255859375, 'y': 300.5348205566406}, {'x': 328.0359191894531, 'y': 306.87030029296875}, {'x': 318.1807556152344, 'y': 307.92620849609375}, {'x': 311.8453063964844, 'y': 310.3899841308594}, {'x': 297.7665100097656, 'y': 316.37347412109375}, {'x': 290.72711181640625, 'y': 317.42938232421875}, {'x': 282.2798156738281, 'y': 311.4458923339844}, {'x': 279.8160400390625, 'y': 307.22222900390625}, {'x': 297.7665100097656, 'y': 307.92620849609375}, {'x': 305.1578674316406, 'y': 299.83087158203125}, {'x': 306.917724609375, 'y': 295.959228515625}, {'x': 294.2467956542969, 'y': 301.5907287597656}, {'x': 281.2239074707031, 'y': 302.6466369628906}, {'x': 272.4246520996094, 'y': 309.68603515625}, {'x': 273.4805908203125, 'y': 317.077392578125}, {'x': 273.4805908203125, 'y': 318.8372497558594}, {'x': 269.2569580078125, 'y': 323.4128723144531}, {'x': 266.4411926269531, 'y': 332.9160461425781}, {'x': 268.5530090332031, 'y': 334.3239440917969}, {'x': 273.8325500488281, 'y': 332.9160461425781}, {'x': 266.0892333984375, 'y': 340.3074035644531}, {'x': 261.1616516113281, 'y': 339.9554443359375}, {'x': 256.23406982421875, 'y': 333.6199645996094}, {'x': 256.5860290527344, 'y': 324.82073974609375}, {'x': 244.61904907226562, 'y': 327.2845458984375}, {'x': 237.93162536621094, 'y': 321.65301513671875}, {'x': 234.41192626953125, 'y': 317.077392578125}, {'x': 235.81980895996094, 'y': 301.5907287597656}, {'x': 229.13238525390625, 'y': 301.23876953125}, {'x': 224.20480346679688, 'y': 314.6136169433594}, {'x': 209.07009887695312, 'y': 326.2286376953125}, {'x': 194.28736877441406, 'y': 327.6365051269531}, {'x': 193.5834197998047, 'y': 322.3569641113281}, {'x': 196.04721069335938, 'y': 315.6695251464844}, {'x': 204.84645080566406, 'y': 319.54119873046875}, {'x': 212.5897979736328, 'y': 315.31756591796875}, {'x': 217.1654052734375, 'y': 306.16632080078125}, {'x': 212.5897979736328, 'y': 306.87030029296875}, {'x': 204.84645080566406, 'y': 306.518310546875}, {'x': 194.63934326171875, 'y': 292.43951416015625}, {'x': 184.7841796875, 'y': 285.7520751953125}, {'x': 165.07386779785156, 'y': 276.6008605957031}, {'x': 156.9785614013672, 'y': 271.6733093261719}, {'x': 151.34703063964844, 'y': 260.4102478027344}, {'x': 146.7714385986328, 'y': 246.33145141601562}, {'x': 149.9391632080078, 'y': 239.64402770996094}, {'x': 152.75491333007812, 'y': 234.36448669433594}, {'x': 153.1068878173828, 'y': 220.2856903076172}, {'x': 154.1627960205078, 'y': 218.1738739013672}, {'x': 138.67611694335938, 'y': 211.8384246826172}, {'x': 135.50840759277344, 'y': 200.22340393066406}, {'x': 136.2123260498047, 'y': 192.83204650878906}, {'x': 133.04461669921875, 'y': 183.68081665039062}, {'x': 138.67611694335938, 'y': 182.97689819335938}, {'x': 134.80445861816406, 'y': 174.17764282226562}, {'x': 133.74855041503906, 'y': 165.02642822265625}, {'x': 137.97219848632812, 'y': 158.6909637451172}, {'x': 133.74855041503906, 'y': 149.8917236328125}, {'x': 133.39657592773438, 'y': 143.90823364257812}, {'x': 137.97219848632812, 'y': 139.68460083007812}, {'x': 144.65960693359375, 'y': 138.98065185546875}, {'x': 138.32415771484375, 'y': 125.25382232666016}, {'x': 140.78794860839844, 'y': 117.86246490478516}, {'x': 147.12339782714844, 'y': 108.35926818847656}]}, {'file_name': 'img03.jpg', 'polygon1': [{'x': 180.36671447753906, 'y': 38.97885513305664}, {'x': 195.6520538330078, 'y': 30.2443904876709}, {'x': 202.20289611816406, 'y': 25.003711700439453}, {'x': 208.7537384033203, 'y': 19.763031005859375}, {'x': 214.86785888671875, 'y': 16.70596694946289}, {'x': 226.22267150878906, 'y': 15.832520484924316}, {'x': 238.88763427734375, 'y': 15.395797729492188}, {'x': 255.04640197753906, 'y': 17.142690658569336}, {'x': 270.7684326171875, 'y': 17.142690658569336}, {'x': 282.9966735839844, 'y': 14.522350311279297}, {'x': 289.1108093261719, 'y': 13.212181091308594}, {'x': 298.71875, 'y': 12.775458335876465}, {'x': 304.8328857421875, 'y': 12.775458335876465}, {'x': 314.0040588378906, 'y': 15.395797729492188}, {'x': 320.5549011230469, 'y': 18.452861785888672}, {'x': 331.4729919433594, 'y': 22.820093154907227}, {'x': 345.4481201171875, 'y': 31.5545597076416}, {'x': 350.2521057128906, 'y': 35.921791076660156}, {'x': 364.6639709472656, 'y': 47.27659606933594}, {'x': 369.9046325683594, 'y': 54.2641716003418}, {'x': 375.58203125, 'y': 66.05570220947266}, {'x': 379.94927978515625, 'y': 76.9737777709961}, {'x': 383.44305419921875, 'y': 87.45513916015625}, {'x': 384.7532043457031, 'y': 96.18960571289062}, {'x': 384.7532043457031, 'y': 116.27888488769531}, {'x': 382.1329040527344, 'y': 128.07040405273438}, {'x': 378.2023620605469, 'y': 141.17210388183594}, {'x': 374.2718811035156, 'y': 159.9512176513672}, {'x': 370.34136962890625, 'y': 175.67324829101562}, {'x': 366.4108581542969, 'y': 187.02806091308594}, {'x': 362.04364013671875, 'y': 197.50941467285156}, {'x': 356.3662109375, 'y': 207.55404663085938}, {'x': 354.1825866699219, 'y': 211.04783630371094}, {'x': 354.1825866699219, 'y': 181.78736877441406}, {'x': 352.43572998046875, 'y': 175.67324829101562}, {'x': 337.5871276855469, 'y': 190.0851287841797}, {'x': 325.35888671875, 'y': 194.8890838623047}, {'x': 316.6244201660156, 'y': 197.50941467285156}, {'x': 310.5102844238281, 'y': 196.63597106933594}, {'x': 305.26959228515625, 'y': 185.28115844726562}, {'x': 303.0859680175781, 'y': 173.48963928222656}, {'x': 299.15545654296875, 'y': 167.81224060058594}, {'x': 290.4209899902344, 'y': 183.9709930419922}, {'x': 284.74359130859375, 'y': 193.5789031982422}, {'x': 279.5028991699219, 'y': 197.50941467285156}, {'x': 264.21759033203125, 'y': 197.50941467285156}, {'x': 248.058837890625, 'y': 198.3828582763672}, {'x': 248.4955596923828, 'y': 197.94613647460938}, {'x': 252.86279296875, 'y': 184.40771484375}, {'x': 253.2995147705078, 'y': 168.2489471435547}, {'x': 252.42605590820312, 'y': 148.59640502929688}, {'x': 239.32437133789062, 'y': 172.17947387695312}, {'x': 228.843017578125, 'y': 181.78736877441406}, {'x': 217.05148315429688, 'y': 184.40771484375}, {'x': 204.82322692871094, 'y': 184.40771484375}, {'x': 193.90513610839844, 'y': 183.9709930419922}, {'x': 186.48085021972656, 'y': 183.9709930419922}, {'x': 177.7463836669922, 'y': 183.9709930419922}, {'x': 176.43621826171875, 'y': 204.06027221679688}, {'x': 169.88536071777344, 'y': 187.02806091308594}, {'x': 165.08140563964844, 'y': 168.2489471435547}, {'x': 159.4040069580078, 'y': 152.96363830566406}, {'x': 155.47349548339844, 'y': 141.17210388183594}, {'x': 151.97970581054688, 'y': 125.4500732421875}, {'x': 150.66954040527344, 'y': 113.22181701660156}, {'x': 152.8531494140625, 'y': 104.05062866210938}, {'x': 152.41644287109375, 'y': 94.00598907470703}, {'x': 153.7266082763672, 'y': 82.65118408203125}, {'x': 158.96728515625, 'y': 71.29637908935547}, {'x': 162.0243377685547, 'y': 61.251747131347656}, {'x': 168.57521057128906, 'y': 50.7703857421875}, {'x': 175.1260528564453, 'y': 42.909366607666016}]}, {'file_name': 'img04.jpg', 'polygon1': [{'x': 180.8374786376953, 'y': 70.70066833496094}, {'x': 172.84466552734375, 'y': 63.70695877075195}, {'x': 175.34242248535156, 'y': 50.7186279296875}, {'x': 181.33705139160156, 'y': 42.72581100463867}, {'x': 193.8258056640625, 'y': 34.73299789428711}, {'x': 203.31729125976562, 'y': 32.2352409362793}, {'x': 210.31100463867188, 'y': 26.74017906188965}, {'x': 224.29843139648438, 'y': 20.246015548706055}, {'x': 235.28855895996094, 'y': 17.248708724975586}, {'x': 253.2723846435547, 'y': 13.252300262451172}, {'x': 261.2652282714844, 'y': 15.250503540039062}, {'x': 271.2562561035156, 'y': 16.24960708618164}, {'x': 283.7449951171875, 'y': 12.7527494430542}, {'x': 293.73602294921875, 'y': 15.250503540039062}, {'x': 303.72705078125, 'y': 12.7527494430542}, {'x': 311.2203063964844, 'y': 15.750054359436035}, {'x': 324.70819091796875, 'y': 17.748260498046875}, {'x': 332.7010192871094, 'y': 26.24062728881836}, {'x': 336.1978759765625, 'y': 32.2352409362793}, {'x': 354.6812744140625, 'y': 38.72940444946289}, {'x': 362.6741027832031, 'y': 50.219078063964844}, {'x': 366.1709289550781, 'y': 61.70875549316406}, {'x': 379.6588134765625, 'y': 74.1975326538086}, {'x': 381.65704345703125, 'y': 80.69169616699219}, {'x': 381.65704345703125, 'y': 85.18765258789062}, {'x': 385.6534423828125, 'y': 92.18136596679688}, {'x': 385.6534423828125, 'y': 107.16790771484375}, {'x': 385.6534423828125, 'y': 118.15802001953125}, {'x': 384.65435791015625, 'y': 133.64410400390625}, {'x': 383.15570068359375, 'y': 147.13198852539062}, {'x': 382.15655517578125, 'y': 156.1239013671875}, {'x': 383.65521240234375, 'y': 161.11941528320312}, {'x': 369.6678161621094, 'y': 172.1095428466797}, {'x': 361.1754455566406, 'y': 184.59832763671875}, {'x': 359.6767883300781, 'y': 201.08349609375}, {'x': 352.6830749511719, 'y': 228.05926513671875}, {'x': 344.69024658203125, 'y': 244.54444885253906}, {'x': 339.1951904296875, 'y': 198.08619689941406}, {'x': 338.19610595703125, 'y': 192.0915985107422}, {'x': 319.213134765625, 'y': 183.59921264648438}, {'x': 306.2248229980469, 'y': 173.6082000732422}, {'x': 300.2301940917969, 'y': 165.11582946777344}, {'x': 287.7414245605469, 'y': 178.60369873046875}, {'x': 281.24725341796875, 'y': 192.0915985107422}, {'x': 279.74859619140625, 'y': 205.07992553710938}, {'x': 272.2553405761719, 'y': 191.59202575683594}, {'x': 272.7548828125, 'y': 170.11134338378906}, {'x': 277.2508544921875, 'y': 150.12930297851562}, {'x': 276.7513122558594, 'y': 142.6360321044922}, {'x': 260.76568603515625, 'y': 137.64051818847656}, {'x': 227.2957305908203, 'y': 134.64321899414062}, {'x': 205.81504821777344, 'y': 135.14276123046875}, {'x': 200.31997680664062, 'y': 140.63783264160156}, {'x': 197.3226776123047, 'y': 152.12750244140625}, {'x': 198.8213348388672, 'y': 162.61807250976562}, {'x': 204.31639099121094, 'y': 167.6135711669922}, {'x': 213.807861328125, 'y': 169.1122283935547}, {'x': 225.2975311279297, 'y': 163.61717224121094}, {'x': 224.79798889160156, 'y': 170.6108856201172}, {'x': 220.30203247070312, 'y': 178.60369873046875}, {'x': 208.81236267089844, 'y': 183.09967041015625}, {'x': 195.82403564453125, 'y': 180.60191345214844}, {'x': 185.3334503173828, 'y': 170.6108856201172}, {'x': 184.8339080810547, 'y': 192.0915985107422}, {'x': 173.34422302246094, 'y': 168.61268615722656}, {'x': 172.34512329101562, 'y': 152.62704467773438}, {'x': 167.84915161132812, 'y': 137.14097595214844}, {'x': 172.34512329101562, 'y': 110.16521453857422}, {'x': 166.3505096435547, 'y': 99.17508697509766}, {'x': 168.8482666015625, 'y': 81.6907958984375}]}, {'file_name': 'img05.jpg', 'polygon1': [{'x': 220.54920959472656, 'y': 27.93947410583496}, {'x': 211.6381378173828, 'y': 29.053359985351562}, {'x': 195.48681640625, 'y': 54.95118713378906}, {'x': 183.23406982421875, 'y': 92.5447998046875}, {'x': 181.2847900390625, 'y': 121.7842788696289}, {'x': 186.01878356933594, 'y': 143.2265625}, {'x': 194.92987060546875, 'y': 158.26400756835938}, {'x': 205.7902374267578, 'y': 174.1368865966797}, {'x': 212.47354125976562, 'y': 182.7694854736328}, {'x': 240.87762451171875, 'y': 188.3389129638672}, {'x': 250.3456573486328, 'y': 184.99725341796875}, {'x': 253.9657745361328, 'y': 171.63063049316406}, {'x': 269.5601501464844, 'y': 166.61814880371094}, {'x': 289.33160400390625, 'y': 171.9091033935547}, {'x': 294.3441162109375, 'y': 168.84591674804688}, {'x': 300.7489318847656, 'y': 181.37713623046875}, {'x': 309.9385070800781, 'y': 178.03546142578125}, {'x': 313.0016784667969, 'y': 166.0612030029297}, {'x': 318.84954833984375, 'y': 160.49179077148438}, {'x': 321.3558044433594, 'y': 159.37789916992188}, {'x': 323.8620300292969, 'y': 152.69459533691406}, {'x': 342.5196228027344, 'y': 151.58070373535156}, {'x': 357.0001220703125, 'y': 134.59396362304688}, {'x': 366.7466125488281, 'y': 109.53154754638672}, {'x': 369.2528381347656, 'y': 90.3170394897461}, {'x': 362.569580078125, 'y': 59.12825393676758}, {'x': 336.39324951171875, 'y': 33.5088996887207}, {'x': 311.0523681640625, 'y': 18.471452713012695}, {'x': 300.470458984375, 'y': 15.408268928527832}, {'x': 282.6483154296875, 'y': 8.446488380432129}, {'x': 256.75048828125, 'y': 9.560373306274414}, {'x': 241.9915008544922, 'y': 13.737442016601562}, {'x': 231.13111877441406, 'y': 17.91451072692871}]}, {'file_name': 'img06.jpg', 'polygon1': [{'x': 217.77630615234375, 'y': 42.28214645385742}, {'x': 226.8032989501953, 'y': 24.228151321411133}, {'x': 243.72891235351562, 'y': 14.072779655456543}, {'x': 262.9112854003906, 'y': 8.430906295776367}, {'x': 288.8639221191406, 'y': 9.559281349182129}, {'x': 299.019287109375, 'y': 20.843027114868164}, {'x': 310.30303955078125, 'y': 35.511898040771484}, {'x': 328.3570251464844, 'y': 42.28214645385742}, {'x': 338.51239013671875, 'y': 47.92401885986328}, {'x': 346.4110107421875, 'y': 61.46451187133789}, {'x': 346.4110107421875, 'y': 78.39013671875}, {'x': 344.1542663574219, 'y': 81.77526092529297}, {'x': 352.05291748046875, 'y': 93.05900573730469}, {'x': 353.1812438964844, 'y': 111.11299896240234}, {'x': 346.4110107421875, 'y': 143.8358612060547}, {'x': 337.384033203125, 'y': 152.86285400390625}, {'x': 329.48541259765625, 'y': 165.27499389648438}, {'x': 324.9718933105469, 'y': 151.73448181152344}, {'x': 312.5597839355469, 'y': 142.70748901367188}, {'x': 297.8908996582031, 'y': 147.2209930419922}, {'x': 288.8639221191406, 'y': 142.70748901367188}, {'x': 275.32342529296875, 'y': 143.8358612060547}, {'x': 257.2694396972656, 'y': 146.09262084960938}, {'x': 240.3437957763672, 'y': 144.96424865722656}, {'x': 217.77630615234375, 'y': 134.80886840820312}, {'x': 235.83029174804688, 'y': 117.88324737548828}, {'x': 251.62754821777344, 'y': 97.57250213623047}, {'x': 252.7559356689453, 'y': 77.26175689697266}, {'x': 242.60055541992188, 'y': 79.51850891113281}, {'x': 229.06005859375, 'y': 73.87664031982422}, {'x': 214.3911895751953, 'y': 77.26175689697266}, {'x': 194.0804443359375, 'y': 90.80226135253906}, {'x': 187.3101806640625, 'y': 112.24137115478516}, {'x': 181.66831970214844, 'y': 134.80886840820312}, {'x': 179.41156005859375, 'y': 168.6601104736328}, {'x': 169.25619506835938, 'y': 152.86285400390625}, {'x': 160.2292022705078, 'y': 139.32237243652344}, {'x': 154.5873260498047, 'y': 117.88324737548828}, {'x': 152.33058166503906, 'y': 106.59950256347656}, {'x': 151.20220947265625, 'y': 87.41712951660156}, {'x': 159.100830078125, 'y': 68.2347640991211}, {'x': 171.51295471191406, 'y': 50.18076705932617}, {'x': 188.43856811523438, 'y': 43.4105224609375}]}, {'file_name': 'img07.jpg', 'polygon1': [{'x': 177.6368865966797, 'y': 155.03334045410156}, {'x': 194.31851196289062, 'y': 204.17654418945312}, {'x': 204.23733520507812, 'y': 223.11245727539062}, {'x': 250.6754150390625, 'y': 231.22784423828125}, {'x': 288.9980773925781, 'y': 230.32614135742188}, {'x': 305.6797180175781, 'y': 211.39022827148438}, {'x': 328.6733093261719, 'y': 190.65089416503906}, {'x': 344.4532470703125, 'y': 162.69789123535156}, {'x': 361.1348876953125, 'y': 127.08033752441406}, {'x': 361.5857238769531, 'y': 95.9713363647461}, {'x': 362.4874267578125, 'y': 89.20851135253906}, {'x': 350.3143615722656, 'y': 57.19780349731445}, {'x': 331.8293151855469, 'y': 35.10590744018555}, {'x': 303.8763122558594, 'y': 22.93282127380371}, {'x': 278.62841796875, 'y': 16.16999626159668}, {'x': 269.611328125, 'y': 13.91572093963623}, {'x': 265.1027526855469, 'y': 17.071706771850586}, {'x': 257.8890686035156, 'y': 12.112300872802734}, {'x': 236.69888305664062, 'y': 8.505460739135742}, {'x': 212.35272216796875, 'y': 17.52256202697754}, {'x': 184.39971923828125, 'y': 33.75334167480469}, {'x': 161.40611267089844, 'y': 61.706356048583984}, {'x': 154.64328002929688, 'y': 97.32390594482422}, {'x': 160.50439453125, 'y': 123.02264404296875}, {'x': 169.52149963378906, 'y': 139.25341796875}]}, {'file_name': 'img08.jpg', 'polygon1': [{'x': 207.6099395751953, 'y': 116.27952575683594}, {'x': 194.42018127441406, 'y': 121.24708557128906}, {'x': 187.56837463378906, 'y': 128.27020263671875}, {'x': 184.14247131347656, 'y': 136.1497802734375}, {'x': 183.457275390625, 'y': 162.015380859375}, {'x': 182.08692932128906, 'y': 174.34864807128906}, {'x': 184.4850616455078, 'y': 182.39950561523438}, {'x': 186.19801330566406, 'y': 192.50595092773438}, {'x': 186.19801330566406, 'y': 196.6170196533203}, {'x': 183.28598022460938, 'y': 188.90875244140625}, {'x': 181.40174865722656, 'y': 194.56149291992188}, {'x': 179.68878173828125, 'y': 184.45506286621094}, {'x': 178.66102600097656, 'y': 173.66346740722656}, {'x': 176.77676391601562, 'y': 161.67279052734375}, {'x': 173.35086059570312, 'y': 149.3395233154297}, {'x': 169.41107177734375, 'y': 140.08956909179688}, {'x': 163.92962646484375, 'y': 130.6683349609375}, {'x': 162.7305450439453, 'y': 119.02025604248047}, {'x': 162.7305450439453, 'y': 111.14066314697266}, {'x': 161.70278930664062, 'y': 78.0806655883789}, {'x': 160.50372314453125, 'y': 64.71963500976562}, {'x': 163.92962646484375, 'y': 52.55767059326172}, {'x': 171.29531860351562, 'y': 43.13642501831055}, {'x': 177.46194458007812, 'y': 36.969791412353516}, {'x': 179.5175018310547, 'y': 31.488340377807617}, {'x': 189.96652221679688, 'y': 24.122644424438477}, {'x': 209.83676147460938, 'y': 12.81715202331543}, {'x': 229.87832641601562, 'y': 8.534769058227539}, {'x': 244.95230102539062, 'y': 9.905131340026855}, {'x': 254.37355041503906, 'y': 14.187514305114746}, {'x': 258.4846496582031, 'y': 11.789380073547363}, {'x': 269.4475402832031, 'y': 9.73383617401123}, {'x': 279.3826599121094, 'y': 11.960675239562988}, {'x': 289.3177795410156, 'y': 15.729171752929688}, {'x': 299.4242248535156, 'y': 19.840259552001953}, {'x': 305.2482604980469, 'y': 24.122644424438477}, {'x': 318.2666931152344, 'y': 34.05777359008789}, {'x': 326.14630126953125, 'y': 42.965126037597656}, {'x': 334.8823547363281, 'y': 55.812278747558594}, {'x': 339.6786193847656, 'y': 67.63165283203125}, {'x': 341.0489807128906, 'y': 77.73808288574219}, {'x': 339.16473388671875, 'y': 87.8445053100586}, {'x': 338.9934387207031, 'y': 93.15465545654297}, {'x': 343.4471130371094, 'y': 107.02957916259766}, {'x': 343.1045227050781, 'y': 127.07112884521484}, {'x': 341.5628662109375, 'y': 137.17755126953125}, {'x': 338.47955322265625, 'y': 147.9691619873047}, {'x': 333.1694030761719, 'y': 158.07557678222656}, {'x': 330.0860900878906, 'y': 163.04315185546875}, {'x': 329.2296142578125, 'y': 171.95050048828125}, {'x': 326.14630126953125, 'y': 182.9134063720703}, {'x': 320.322265625, 'y': 195.58926391601562}, {'x': 318.6092834472656, 'y': 197.3022003173828}, {'x': 318.6092834472656, 'y': 189.5939178466797}, {'x': 321.6925964355469, 'y': 176.40419006347656}, {'x': 322.3777770996094, 'y': 167.15423583984375}, {'x': 322.8916931152344, 'y': 152.59413146972656}, {'x': 323.06298828125, 'y': 140.08956909179688}, {'x': 322.549072265625, 'y': 138.205322265625}, {'x': 317.5815124511719, 'y': 140.4321746826172}, {'x': 311.4148864746094, 'y': 135.80718994140625}, {'x': 311.4148864746094, 'y': 133.92294311523438}, {'x': 314.66949462890625, 'y': 127.9276123046875}, {'x': 305.2482604980469, 'y': 129.64056396484375}, {'x': 303.02142333984375, 'y': 128.27020263671875}, {'x': 310.55841064453125, 'y': 119.70542907714844}, {'x': 313.98431396484375, 'y': 114.2239761352539}, {'x': 301.8223571777344, 'y': 121.24708557128906}, {'x': 290.00299072265625, 'y': 121.07579040527344}, {'x': 279.553955078125, 'y': 115.76563262939453}, {'x': 270.4753112792969, 'y': 115.25175476074219}, {'x': 256.77166748046875, 'y': 112.85362243652344}, {'x': 249.9198760986328, 'y': 110.7980728149414}, {'x': 236.558837890625, 'y': 116.96470642089844}, {'x': 221.8274383544922, 'y': 118.50636291503906}]}, {'file_name': 'img09.jpg', 'polygon1': [{'x': 224.47726440429688, 'y': 154.68331909179688}, {'x': 217.72874450683594, 'y': 166.75962829589844}, {'x': 216.30801391601562, 'y': 173.15296936035156}, {'x': 196.06243896484375, 'y': 166.40443420410156}, {'x': 185.40687561035156, 'y': 165.33888244628906}, {'x': 180.43426513671875, 'y': 165.33888244628906}, {'x': 179.72389221191406, 'y': 161.07666015625}, {'x': 170.48907470703125, 'y': 157.52479553222656}, {'x': 164.09573364257812, 'y': 153.2625732421875}, {'x': 156.2816619873047, 'y': 143.31736755371094}, {'x': 158.4127655029297, 'y': 118.45438385009766}, {'x': 168.3579559326172, 'y': 100.69510650634766}, {'x': 175.8168487548828, 'y': 87.9084243774414}, {'x': 181.1446533203125, 'y': 76.54248809814453}, {'x': 187.53797912597656, 'y': 67.30766296386719}, {'x': 202.8109588623047, 'y': 55.94173049926758}, {'x': 217.37356567382812, 'y': 52.389869689941406}, {'x': 226.25320434570312, 'y': 45.99653244018555}, {'x': 246.1436004638672, 'y': 46.35171890258789}, {'x': 258.9302673339844, 'y': 53.81061553955078}, {'x': 271.006591796875, 'y': 59.84877014160156}, {'x': 282.3725280761719, 'y': 60.559139251708984}, {'x': 289.8314208984375, 'y': 60.91432189941406}, {'x': 306.8803405761719, 'y': 70.50433349609375}, {'x': 308.6562805175781, 'y': 81.51509094238281}, {'x': 318.9566345214844, 'y': 97.4984359741211}, {'x': 319.31182861328125, 'y': 103.89178466796875}, {'x': 325.7051696777344, 'y': 109.21955871582031}, {'x': 332.0985107421875, 'y': 113.4817886352539}, {'x': 338.4918518066406, 'y': 126.97884368896484}, {'x': 338.4918518066406, 'y': 139.76551818847656}, {'x': 334.2296142578125, 'y': 146.86923217773438}, {'x': 325.7051696777344, 'y': 149.00035095214844}, {'x': 317.1806945800781, 'y': 158.94554138183594}, {'x': 307.5906982421875, 'y': 175.28408813476562}, {'x': 301.1973571777344, 'y': 190.55706787109375}, {'x': 293.73846435546875, 'y': 203.69891357421875}, {'x': 301.1973571777344, 'y': 190.20187377929688}, {'x': 299.0662536621094, 'y': 178.1255645751953}, {'x': 294.0936584472656, 'y': 175.28408813476562}, {'x': 282.72772216796875, 'y': 178.8359375}, {'x': 275.268798828125, 'y': 183.45335388183594}, {'x': 272.0721435546875, 'y': 185.9396514892578}, {'x': 262.4821472167969, 'y': 205.11965942382812}, {'x': 259.28546142578125, 'y': 202.98855590820312}, {'x': 250.4058380126953, 'y': 185.58445739746094}, {'x': 242.23655700683594, 'y': 169.956298828125}, {'x': 236.5535888671875, 'y': 156.81442260742188}, {'x': 228.739501953125, 'y': 163.56295776367188}]}, {'file_name': 'img10.jpg', 'polygon1': [{'x': 274.713134765625, 'y': 18.689054489135742}, {'x': 269.34417724609375, 'y': 8.398496627807617}, {'x': 256.8165283203125, 'y': 9.293327331542969}, {'x': 255.02687072753906, 'y': 16.004560470581055}, {'x': 251.44754028320312, 'y': 13.76748275756836}, {'x': 240.26214599609375, 'y': 15.109728813171387}, {'x': 231.76126098632812, 'y': 19.1364688873291}, {'x': 225.05003356933594, 'y': 24.505456924438477}, {'x': 222.81295776367188, 'y': 28.979610443115234}, {'x': 212.5223846435547, 'y': 28.084779739379883}, {'x': 204.9163360595703, 'y': 33.90118408203125}, {'x': 188.36195373535156, 'y': 41.50724792480469}, {'x': 184.7826385498047, 'y': 48.218482971191406}, {'x': 187.4671173095703, 'y': 50.45555877685547}, {'x': 180.75588989257812, 'y': 50.00814437866211}, {'x': 182.09812927246094, 'y': 58.509037017822266}, {'x': 182.09812927246094, 'y': 62.98319625854492}, {'x': 174.4920654296875, 'y': 73.27375030517578}, {'x': 170.91275024414062, 'y': 84.45913696289062}, {'x': 169.12307739257812, 'y': 97.8816146850586}, {'x': 175.38690185546875, 'y': 116.22563934326172}, {'x': 178.51881408691406, 'y': 140.38609313964844}, {'x': 180.75588989257812, 'y': 143.07058715820312}, {'x': 185.23004150390625, 'y': 136.35934448242188}, {'x': 185.23004150390625, 'y': 125.62137603759766}, {'x': 187.4671173095703, 'y': 115.77822875976562}, {'x': 197.7576904296875, 'y': 114.43598175048828}, {'x': 220.57586669921875, 'y': 118.01530456542969}, {'x': 246.97340393066406, 'y': 123.83171081542969}, {'x': 269.34417724609375, 'y': 129.6481170654297}, {'x': 278.7398986816406, 'y': 133.22744750976562}, {'x': 280.97698974609375, 'y': 143.07058715820312}, {'x': 280.0821228027344, 'y': 155.1508026123047}, {'x': 289.92529296875, 'y': 163.6516876220703}, {'x': 301.1106872558594, 'y': 169.4680938720703}, {'x': 309.611572265625, 'y': 187.36473083496094}, {'x': 308.2693176269531, 'y': 198.9975128173828}, {'x': 324.8236999511719, 'y': 178.8638153076172}, {'x': 329.7452697753906, 'y': 168.57327270507812}, {'x': 333.3245849609375, 'y': 166.78359985351562}, {'x': 335.5616760253906, 'y': 167.67843627929688}, {'x': 342.7203063964844, 'y': 153.36114501953125}, {'x': 344.06256103515625, 'y': 143.5179901123047}, {'x': 347.64190673828125, 'y': 135.01710510253906}, {'x': 353.4582824707031, 'y': 125.62137603759766}, {'x': 357.9324645996094, 'y': 109.51441955566406}, {'x': 359.72210693359375, 'y': 93.85486602783203}, {'x': 359.72210693359375, 'y': 79.9849853515625}, {'x': 353.4582824707031, 'y': 71.03667449951172}, {'x': 348.5367126464844, 'y': 58.956451416015625}, {'x': 340.03582763671875, 'y': 42.40208053588867}, {'x': 329.7452697753906, 'y': 31.664106369018555}, {'x': 317.2176208496094, 'y': 23.163209915161133}, {'x': 303.3477478027344, 'y': 18.689054489135742}]}]

entries = {}
for idx, files in enumerate(data['annotations']):
    entries[files['file_name']]=[]
    for polygon in files['polygon1']:
        entries[files['file_name']].append(tuple(polygon.values()))


width = height = 512

for name, data in entries.items():
    img = Image.new('L', (width, height), 0)
    ImageDraw.Draw(img).polygon(data, outline=1, fill=1)
    img.save(sys.argv[2]+'/'+name)
