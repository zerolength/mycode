import re
#63/64
#need to rewrite in dict
element=["電撃","重力","焼夷","冷撃"]

_narokozaka=['yotsuyu','SITARA','fumika']
_verbena=['ayaka','mutsumi','aika']
_murakumo=['kaede','RIN','rei']
_nakamo=['yumi', 'yayoi', 'touka']

firm_ls = [
        f'{_narokozaka=}'.split('=')[0],
        f'{_verbena=}'.split('=')[0],
        f'{_murakumo=}'.split('=')[0],
        f'{_nakamo=}'.split('=')[0],
    ]
print(firm_ls)

narukozakaGrp = [_narokozaka,_verbena,_murakumo]
narukozakaGrp.append((_nakamo))
print(narukozakaGrp)

new_firm=input("会社名：")

new_members = input("社員：")
new_members = re.split(';|,|\*|\n',new_members)

locals()[new_firm] = new_members
firm_ls.append(("_"+new_firm))

print(locals()[new_firm])
print(firm_ls)
temp = locals()[new_firm]
narukozakaGrp.append(temp)
print(narukozakaGrp)

pick=input("2 numbers seperated by space")

pick=pick.split()
pick=[eval(i) for i in pick ]
pick=[i-1 for i in pick]

print(narukozakaGrp[pick[0]][pick[1]])

shooting_gear=["rifle","bazooka", "dual", "sniper"]
close_gear=["両手剣","hammer","lance","片手剣"]

close_gear.pop(1)
print(close_gear)
close_gear.insert(1,"hammer")
print(close_gear)

shooting_gearPop=[shooting_gear.pop(2)]
shooting_gearPop.append(shooting_gear.pop(2))
print(shooting_gearPop)
print(shooting_gear)
shooting_gear.extend(shooting_gearPop)
print(shooting_gear)

