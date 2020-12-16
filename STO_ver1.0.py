import os
from numpy import array
from numpy import cross
from numpy import linalg
from numpy import cos
from numpy import sin
from numpy import pi
# 遍历所有文件，如果后缀为s2k，则将这一文件的（文件名.后缀）存到变量filename中
# 如果文件夹中有两个s2k文件，则只对其中一个文件进行操作
# ------------------------------------------------------------------------------
# 获取工作文件夹下的所有文件：文件名.后缀
files = os.listdir(os.getcwd())
# 遍历所有文件，获得所有后缀
exten = []
for file in files:
    # 提取文件夹内所有文件的后缀存到exten中
    exten.append(file.split('.')[1])
if 's2k' in exten:
    filename = files[exten.index('s2k')]
    print('已找到文件%s    %s Has Been Found' % (filename, filename))
else:
    print('当前文件夹下没有s2k文件    S2K File NOT Found')
# ------------------------------------------------------------------------------


# 查找“目标关键字”，并返回目标关键字所在行下一行的行号
# 其中keyword是srt，lines是由readlines()所生成的一个表格
# ------------------------------------------------------------------------------
def SearchKeyword(keyword, lines):
    for index, line in enumerate(lines):
        if keyword in line:
            # 目标关键字在文件的第index行（注意python中计数从0开始，即文件中第一行的index为0）
            # 目标关键字所在行下一行的行号为index + 1
            startline = index + 1
            break
    else:
        # startline = f"未在文件中发现{key_word}"，返回-1，建模关键信息若返回-1则应报错
        startline = -1
    return startline
# ------------------------------------------------------------------------------


# 计算坐标转换向量(局部轴旋转角默认为0)
# 其中a为i节点的节点编号，b为j节点的节点编号,degree为用户指定的局部轴（默认为0）
# ------------------------------------------------------------------------------
def GeomTransfVector(a, b, deg='0'):
    d_x = float(node_lib[node_lib.index(b) + 1]) - float(node_lib[node_lib.index(a) + 1])
    d_y = float(node_lib[node_lib.index(b) + 2]) - float(node_lib[node_lib.index(a) + 2])
    d_z = float(node_lib[node_lib.index(b) + 3]) - float(node_lib[node_lib.index(a) + 3])
    # 局部1轴由节点I指向节点J
    l_x = array([d_x, d_y, d_z])
    # 整体z轴
    g_z = array([0, 0, 1])
    # Sap2000中如果单元竖直，则局部y轴与整体x轴相同，局部z轴则可由局部x轴叉乘局部y轴得到
    if d_x == 0 and d_y == 0:
        l_y = array([1, 0, 0])
        l_z = cross(l_x, l_y)
    # 其他情况下局部x轴与局部y轴组成的平面为竖直平面（即法向量水平），这时局部z轴可由局部x轴与整体z轴叉乘得到
    else:
        l_z = cross(l_x, g_z)
    # 建模时还可能对局部轴进行旋转，这里用到了罗德里格旋转公式
    l_z_rot = l_z * cos(float(deg) / 180 * pi) + cross(l_x, l_z) * sin(float(deg) / 180 * pi)
    # 最后返回标准化后的局部z轴
    return l_z_rot / linalg.norm(l_z_rot)
# ------------------------------------------------------------------------------


# 计算link单元的方向向量(局部轴旋转角默认为0)
# 其中a为i节点的节点编号，b为j节点的节点编号,degree为用户指定的局部轴（默认为0）
# ------------------------------------------------------------------------------
def LinkVector(a, b, deg='0'):
    d_x = float(node_lib[node_lib.index(b) + 1]) - float(node_lib[node_lib.index(a) + 1])
    d_y = float(node_lib[node_lib.index(b) + 2]) - float(node_lib[node_lib.index(a) + 2])
    d_z = float(node_lib[node_lib.index(b) + 3]) - float(node_lib[node_lib.index(a) + 3])
    # 局部1轴由节点I指向节点J
    l_x = array([d_x, d_y, d_z])
    # 整体z轴
    g_z = array([0, 0, 1])
    # Sap2000中如果link竖直，则局部y轴与整体x轴相同，局部z轴则可由局部x轴叉乘局部y轴得到
    if d_x == 0 and d_y == 0:
        l_y = array([1, 0, 0])
        l_z = cross(l_x, l_y)
    # 其他情况下局部x轴与局部y轴组成的平面为竖直平面（即法向量水平），这时局部z轴可由局部x轴与整体z轴叉乘得到
    else:
        l_z = cross(l_x, g_z)
    # 建模时还可能对局部轴进行旋转，这里用到了罗德里格旋转公式
    l_z_rot = l_z * cos(float(deg) / 180 * pi) + cross(l_x, l_z) * sin(float(deg) / 180 * pi)
    # 旋转后的局部y轴则可由旋转后的局部z轴与局部x轴叉乘得到
    l_y_rot = cross(l_z_rot, l_x)
    # 最后返回标准化后的局部y轴
    return l_y_rot / linalg.norm(l_y_rot)
# ------------------------------------------------------------------------------


# 欧拉梁的建立
# ------------------------------------------------------------------------------
def ElasticBeamColumn(frame, sec, matoverwrite, nodei, nodej):
    result = sec_lib.index(sec)
    a = sec_lib[result + 3]
    j = sec_lib[result + 4]
    Iy = sec_lib[result + 5]
    Iz = sec_lib[result + 6]
    if matoverwrite == 'Default':
        e = sec_lib[result + 1]
        g = sec_lib[result + 2]
    else:
        e = mat_lib[mat_lib.index(matoverwrite) + 1]
        g = mat_lib[mat_lib.index(matoverwrite) + 2]
    element.write('element elasticBeamColumn ' + frame + ' ' + nodei + ' ' + nodej + ' ' + a + ' ' + e + ' ' + g + ' ' + j + ' ' + Iy + ' ' + Iz + ' ' + frame + '\n')
# ------------------------------------------------------------------------------


# 拉索单元建立
# ------------------------------------------------------------------------------
def CableElement(frame, sec, matoverwrite, mat_total, nodei, nodej):
    result = sec_lib.index(sec)
    a = sec_lib[result + 3]
    if matoverwrite == 'Default':
        e = sec_lib[result + 1]
    else:
        e = mat_lib[mat_lib.index(matoverwrite) + 1]
    initforce = float(initial_force[frame])
    initstrain = - initforce / float(e) / float(a)
    Material.write('uniaxialMaterial ElasticPP ' + str(mat_total) + ' ' + e + ' 1 -1 ' + str(initstrain) + '\n')
    element.write('element truss ' + frame + ' ' + nodei + ' ' + nodej + ' ' + a + ' ' + str(mat_total) + '\n')
# ------------------------------------------------------------------------------


# 拉索单元建立
# ------------------------------------------------------------------------------
def CorotCableElement(frame, sec, matoverwrite, mat_total, nodei, nodej):
    result = sec_lib.index(sec)
    a = sec_lib[result + 3]
    if matoverwrite == 'Default':
        e = sec_lib[result + 1]
    else:
        e = mat_lib[mat_lib.index(matoverwrite) + 1]
    initforce = float(initial_force[frame])
    initstrain = - initforce / float(e) / float(a)
    Material.write('uniaxialMaterial ElasticPP ' + str(mat_total) + ' ' + e + ' 1 -1 ' + str(initstrain) + '\n')
    element.write('element corotTruss ' + frame + ' ' + nodei + ' ' + nodej + ' ' + a + ' ' + str(mat_total) + '\n')
# ------------------------------------------------------------------------------


'''
目标关键字，即s2k文件中包含的模型信息所在的TABLE;
SAP模型中需要至少包含：节点、节点质量、弹性材料特性、弹性截面特性、弹性梁单元;
------------------------------------------------------------------------------
searchtable = ['MATERIAL PROPERTIES 02 - BASIC MECHANICAL PROPERTIES',--------√
               'FRAME SECTION PROPERTIES 01 - GENERAL',-----------------------√
               'LINK PROPERTY DEFINITIONS 04 - DAMPER',-----------------------√
               'LINK PROPERTY DEFINITIONS 10 - PLASTIC (WEN)',----------------√
               'GROUPS 1 - DEFINITIONS',
               'GROUPS 2 - ASSIGNMENTS',
               'JOINT RESTRAINT ASSIGNMENTS',---------------------------------√
               'JOINT COORDINATES',-------------------------------------------√
               'CONNECTIVITY - FRAME',----------------------------------------√
               'CONNECTIVITY - LINK',-----------------------------------------√
               'LINK PROPERTY ASSIGNMENTS',-----------------------------------√
               'JOINT CONSTRAINT ASSIGNMENTS',--------------------------------√
               'JOINT SPRING ASSIGNMENTS 2 - COUPLED',------------------------√
               'FRAME SECTION ASSIGNMENTS',-----------------------------------√
               'FRAME RELEASE ASSIGNMENTS 1 - GENERAL',-----------------------√
               'FRAME LOCAL AXES ASSIGNMENTS 1 - TYPICAL',--------------------√
               'LINK LOCAL AXES ASSIGNMENTS 1 - TYPICAL',---------------------√
               'FRAME P-DELTA FORCE ASSIGNMENTS',-----------------------------√
               'ASSEMBLED JOINT MASSES',--------------------------------------√
               'MODAL PARTICIPATING MASS RATIOS']
------------------------------------------------------------------------------
'''


# 接口程序主体，打开s2k文件并简称为f
# ------------------------------------------------------------------------------
with open(filename) as f:
    # 读取s2k文件的所有行
    lines = f.readlines()
    # 指定内容下一行的行号
    a = SearchKeyword('JOINT COORDINATES', lines)
    # 节点定义为重要信息，若s2k中不存在该信息，则程序不再运行
    if a == -1:
        print('s2k文件中没有定义节点信息    Node Definition NOT Found')
    else:
        with open('Node.tcl', 'w') as N:
            # 节点表格，后面建模要用
            node_lib = []
            # 节点总数
            node_total = 0
            # 从第a行开始遍历
            for line in lines[a:]:
                # 如果不是空行就一直遍历下去
                if not line.isspace():
                    result = line.split()
                    n = result[0].split('=')[1]
                    x = result[3].split('=')[1]
                    y = result[4].split('=')[1]
                    z = result[5].split('=')[1]
                    node_lib.append(n)
                    node_lib.append(x)
                    node_lib.append(y)
                    node_lib.append(z)
                    N.write('node ' + n + ' ' + x + ' ' + y + ' ' + z + '\n')
                    node_total += 1
                # 如果是空行则循环结束，节点文件已生成
                else:
                    print('节点文件已生成    Node File Has Been Created')
                    break
        # 指定内容下一行的行号
        a = SearchKeyword('ASSEMBLED JOINT MASSES', lines)
        # 节点质量定义为重要信息，若s2k中不存在该信息，则程序不再运行
        if a == -1:
            print('s2k文件中没有定义质量信息    Mass Definition NOT Found')
        else:
            M = open('Mass.tcl', 'w')
            G = open('Gravity.tcl', 'w')
            G.write('pattern Plain 1 Linear {' + '\n')
            # 从第a行开始遍历
            for line in lines[a:]:
                # 判断不是空行以及不是合计质量（SumAccel)
                if 'Sum' not in line and not line.isspace():
                    result = line.split()
                    n = result[0].split('=')[1]
                    x = result[2].split('=')[1]
                    y = result[3].split('=')[1]
                    z = result[4].split('=')[1]
                    M.write('mass ' + n + ' ' + x + ' ' + y + ' ' + z + ' 0 0 0' + '\n')
                    G.write('    load' + ' ' + n + ' 0 0 ' + str( - float(z) * 9.81) + ' ' + ' 0 0 0' + '\n')
                else:
                    print('节点质量文件已生成    Joint Mass File Has Been Created')
                    break
            G.write('}' + '\n')
            M.close()
            G.close()

            # 指定内容下一行的行号
            a = SearchKeyword('MATERIAL PROPERTIES 02 - BASIC MECHANICAL PROPERTIES', lines)
            # 弹性材料特性为重要信息，若s2k中不存在该信息，则程序不再运行
            if a == -1:
                print('s2k文件中没有定义弹性材料    Elastic Material NOT FOUND')
            else:
                with open('Material.tcl', 'w') as Ma:
                    # 节点表格，后面建模要用
                    mat_lib = []
                    # 材料总数
                    mat_total = 0
                    # 从第a行开始遍历
                    for line in lines[a:]:
                        # 如果不是空行就一直遍历下去
                        if not line.isspace():
                            result = line.split()
                            n = result[0].split('=')[1]
                            e = result[3].split('=')[1]
                            # 对于一般材料g_or_a为g，但对于高强钢丝g_or_a为a
                            g_or_a = result[4].split('=')[1]
                            # 如果g_or_a是g的话，就把g_or_a赋给g
                            if float(g_or_a) * 2 * (1 + 0.4) > float(e):
                                g = g_or_a
                                v = result[5].split('=')[1]
                            # 否则就自己算一个g，但对于高强钢丝剪切模量没什么用，这里为了后面编程方便
                            else:
                                g = float(e[1]) / 2 / (1 + 0.3)
                                v = 0.3
                            mat_total += 1
                            mat_lib.append(str(mat_total))
                            mat_lib.append(n)
                            mat_lib.append(e)
                            mat_lib.append(str(g))
                            Ma.write('nDMaterial ElasticIsotropic ' + str(mat_total) + ' ' + e + ' ' + str(v) + '\n')
                        else:
                            print('弹性材料文件已生成    Elastic Material File Has Been Created')
                            break
                # 指定内容下一行的行号
                a = SearchKeyword('FRAME SECTION PROPERTIES 01 - GENERAL', lines)
                # 截面特性特性为重要信息，若s2k中不存在该信息，则程序不再运行
                if a == -1:
                    print('s2k文件中没有定义弹性截面   Elastic Section Property NOT FOUND')
                else:
                    with open('Section.tcl', 'w') as S:
                        # 截面表格，后面建模要用
                        sec_lib = []
                        # 截面总数
                        sec_total = 0
                        # 从第a行开始遍历
                        for line in lines[a::2]:
                            # 如果不是空行就一直遍历下去
                            if not line.isspace():
                                result = line.split()
                                n = result[0].split('=')[1]
                                mat = result[1].split('=')[1]
                                a = result[5].split('=')[1]
                                J = result[6].split('=')[1]
                                Iy = result[8].split('=')[1]
                                Iz = result[7].split('=')[1]
                                ShearArea_y = result[10].split('=')[1]
                                ShearArea_z = result[11].split('=')[1]
                                sec_total += 1
                                sec_lib.append(str(sec_total))
                                sec_lib.append(n)
                                sec_lib.append(mat_lib[mat_lib.index(mat) + 1])
                                sec_lib.append(mat_lib[mat_lib.index(mat) + 2])
                                sec_lib.append(a)
                                sec_lib.append(J)
                                sec_lib.append(Iy)
                                sec_lib.append(Iz)
                                sec_lib.append(ShearArea_y)
                                sec_lib.append(ShearArea_z)
                                S.write('section Elastic ' + str(sec_total) + ' ' + mat_lib[mat_lib.index(mat) + 1] + ' ' + a + ' ' + Iz + ' ' + Iy + ' ' + mat_lib[mat_lib.index(mat) + 2] + ' ' + J + '\n')
                            else:
                                print('弹性截面文件已生成    Elastic Section File Has Been Created')
                                break
                    
                    # 指定内容下一行的行号
                    a = SearchKeyword('CONNECTIVITY - FRAME', lines)
                    # 单元定义为重要信息，若s2k中不存在该信息，则程序不再运行
                    if a == -1:
                        print('s2k文件中没有定义单元   Element Definition NOT FOUND')
                    else:
                        # 存储i节点的字典
                        nodei = {}
                        # 存储j节点的字典
                        nodej = {}
                        # 从第a行开始遍历
                        for line in lines[a:]:
                            # 如果不是空行就一直遍历下去
                            if not line.isspace():
                                result = line.split()
                                n = result[0].split('=')[1]
                                i = result[1].split('=')[1]
                                j = result[2].split('=')[1]
                                nodei[n] = i
                                nodej[n] = j
                            else:
                                break
                        # 单元总数
                        ele_total = len(nodei)

                        a = SearchKeyword('FRAME LOCAL AXES ASSIGNMENTS 1 - TYPICAL', lines)
                        # 单元局部轴转动字典
                        ele_local = {}
                        # 如果没有对单元的局部轴进行调整
                        if a == -1:
                            pass
                        else:
                            # 从第a行开始遍历
                            for line in lines[a:]:
                                # 如果不是空行就一直遍历下去
                                if not line.isspace():
                                    result = line.split()
                                    frame = result[0].split('=')
                                    degree = result[1].split('=')
                                    ele_local[frame[1]] = degree[1]
                                else:
                                    break

                        '''
                        print('请输入几何变换方式：')
                        print('1.Linear Transformation;')
                        print('2、PDelta Transformation;')
                        print('3、Corotational Transformation;')
                        # flag = input()
                        '''
                        # 暂时均考虑Corotational这一种几何变换方式
                        flag = 3
                        with open('Geomtransf.tcl', 'w') as g:
                            # 对单元进行遍历
                            for ele in nodei.keys():
                                # 如果单元号不在单元局部轴转动字典的键列表中
                                if ele not in ele_local.keys():
                                    # 如果没有定义特殊的局部坐标轴
                                    v_x = GeomTransfVector(nodei[ele], nodej[ele])[0]
                                    v_y = GeomTransfVector(nodei[ele], nodej[ele])[1]
                                    v_z = GeomTransfVector(nodei[ele], nodej[ele])[2]
                                    if int(flag) == 1:
                                        g.write('geomTransf Linear ' + ele + ' ' + str(v_x) + ' ' + str(v_y) + ' ' + str(v_z) + '\n')
                                    elif int(flag) == 2:
                                        g.write('geomTransf PDelta ' + ele + ' ' + str(v_x) + ' ' + str(v_y) + ' ' + str(v_z) + '\n')
                                    else:
                                        g.write('geomTransf Corotational ' + ele + ' ' + str(v_x) + ' ' + str(v_y) + ' ' + str(v_z) + '\n')
                                else:
                                    # 如果定义了特殊的局部坐标轴
                                    v_x = GeomTransfVector(nodei[ele], nodej[ele], ele_local[ele])[0]
                                    v_y = GeomTransfVector(nodei[ele], nodej[ele], ele_local[ele])[1]
                                    v_z = GeomTransfVector(nodei[ele], nodej[ele], ele_local[ele])[2]
                                    if int(flag) == 1:
                                        g.write('geomTransf Linear ' + ele + ' ' + str(v_x) + ' ' + str(v_y) + ' ' + str(v_z) + '\n')
                                    elif int(flag) == 2:
                                        g.write('geomTransf PDelta ' + ele + ' ' + str(v_x) + ' ' + str(v_y) + ' ' + str(v_z) + '\n')
                                    else:
                                        g.write('geomTransf Corotational ' + ele + ' ' + str(v_x) + ' ' + str(v_y) + ' ' + str(v_z) + '\n')
                        print('局部坐标文件已生成    Geomtransf File Has Been Created')


                        a = SearchKeyword('FRAME P-DELTA FORCE ASSIGNMENTS', lines)
                        # 单元初内力字典
                        # 由初内力到初应变的结果是否可信，后期应该是需要优化的！！！！！
                        initial_force = {}
                        # 从第a行开始遍历
                        for line in lines[a:]:
                            # 如果不是空行就一直遍历下去
                            if not line.isspace():
                                result = line.split()
                                frame = result[0].split('=')[1]
                                force = result[4].split('=')[1]
                                initial_force[frame] = force
                            else:
                                break

                        # 目前只考虑了T M2 M3全释放（即缆索系统与其余结构铰接）
                        a = SearchKeyword('FRAME RELEASE ASSIGNMENTS 1 - GENERAL', lines)
                        # 梁端释放表格
                        release = []
                        # 从第a行开始遍历
                        for line in lines[a:]:
                            # 如果不是空行就一直遍历下去
                            if not line.isspace():
                                result = line.split()
                                frame = result[0].split('=')[1]
                                release.append(frame)
                            else:
                                break

                        '''
                        print('是否需要考虑除缆索之外的单元的初内力，如主梁、桥塔、桥墩？')
                        print('1、是;')
                        print('2、否;')
                        flag1 = input()
                        '''
                        # 好像大家都不去考虑除缆索外的初内力，后期有待优化！！！
                        flag1 = 2
                        a = SearchKeyword('FRAME SECTION ASSIGNMENTS', lines)
                        element = open('Element.tcl', 'w')
                        Material = open('Material.tcl', 'a')
                        # 从第a行开始遍历
                        for line in lines[a:]:
                            # 如果不是空行就一直遍历下去
                            if not line.isspace():
                                result = line.split()
                                frame = result[0].split('=')[1]
                                i = nodei[frame]
                                j = nodej[frame]
                                sec = result[3].split('=')[1]
                                # 材料覆盖项
                                matoverwrite = result[5].split('=')[1]
                                if int(flag1) == 1:
                                    # 要考虑除缆索之外的单元的初内力(此时结构中考虑初内力的缆索，考虑初内力的梁柱，以及不考虑初内力的其他单元)
                                    if frame not in initial_force.keys():
                                        # 不需要指定初内力({单元|端部释放} 属于 {单元|指定初内力})
                                        ElasticBeamColumn(frame, sec, matoverwrite, i, j)
                                    elif frame in release:
                                        pass
                                        # 缆索系统
                                        # uniaxialMaterial ElasticPP
                                        # 这时候应该给的是应力应变关系（模量）
                                        # element truss
                                        # element corotTruss
                                        # 几何非线性桁架
                                    else:
                                        pass
                                        # 桥塔、桥墩
                                        # uniaxialMaterial ElasticPP
                                        # uniaxialMaterial Elastic
                                        # uniaxialMaterial Elastic
                                        # uniaxialMaterial Elastic
                                        # uniaxialMaterial Elastic
                                        # uniaxialMaterial Elastic
                                        # 这时候应该给的是力位移关系（刚度）
                                        # section Aggregator
                                        # element nonlinearBeamColumn
                                else:
                                    # 不考虑除缆索之外的单元的初内力(此时结构中只有考虑初内力的缆索，以及不考虑初内力的其他单元)
                                    if frame not in release:
                                        # 除了缆索系统外都是普通梁
                                        ElasticBeamColumn(frame, sec, matoverwrite, i, j)
                                    else:
                                        mat_total += 1
                                        if flag == 1:
                                            CableElement(frame, sec, matoverwrite, mat_total, i, j)
                                        else:
                                            CorotCableElement(frame, sec, matoverwrite, mat_total, i, j)
                            else:
                                break
                        frame_max = int(frame)
                        element.close()
                        Material.close()
                        print('弹性梁单元文件已生成    Elastic Element File Has Been Created')


                        a = SearchKeyword('JOINT CONSTRAINT ASSIGNMENTS', lines)
                        if a == -1:
                            print('模型中没有定义Body约束    No Body Constaints Are Available')
                        else:
                            # body字典 格式为{'节点号':'约束名'}
                            nodebodys = {}
                            # 从第a行开始遍历
                            for line in lines[a:]:
                                # 如果不是空行就一直遍历下去
                                if not line.isspace():
                                    result = line.split()
                                    # 返回节点号
                                    n = result[0].split('=')
                                    # 返回body名称
                                    bodyname = result[1].split('=')
                                    # 生成字典
                                    nodebodys[n[1]] = bodyname[1]
                                else:
                                    break
                            # 对字典按body名称排序，返回一个列表 【（节点，body名）】
                            nodebodys = sorted(nodebodys.items(), key=lambda x: x[1])
                            with open('Body.tcl', 'w') as body:
                                nodes = []
                                # 将第一个body名赋值给指针
                                pointer = nodebodys[0][1]
                                # 遍历元组，如果元组中第二个元素——body名与指针中的相同，则将元组中第一个元素——节点号存到nodes中
                                for nodebody in nodebodys:
                                    if nodebody[1] == pointer:
                                        # pointer[0] = i[1]
                                        nodes.append(nodebody[0])
                                    else:
                                        # 先把nodes中的节点写到body文件中
                                        length = len(nodes)
                                        for le in range(length - 1):
                                            body.write('rigidLink beam' + ' ' + nodes[0] + ' ' + nodes[le + 1] + '\n')
                                        # 还原nodes，并将返回False的那个节点存进去，
                                        nodes = []
                                        nodes.append(nodebody[0])
                                        # 指针改为新的body名称
                                        pointer = nodebody[1]
                                # for循环结束后把最后一次循环的nodes中的节点写到body文件中
                                length = len(nodes)
                                for le in range(length - 1):
                                    body.write('rigidLink beam' + ' ' + nodes[0] + ' ' + nodes[le + 1] + '\n')
                            print('Body约束文件已生成    Body Constaint File Has Been Created')


                        # 指定内容下一行的行号，目前支持damper与wen
                        a = SearchKeyword('CONNECTIVITY - LINK', lines)
                        if a == -1:
                            print('模型中没有定义link单元    No Links Are Available')
                        else:
                            # 存储i节点的字典
                            link_nodei = {}
                            # 存储j节点的字典
                            link_nodej = {}
                            # 从第a行开始遍历
                            for line in lines[a:]:
                                # 如果不是空行就一直遍历下去
                                if not line.isspace():
                                    result = line.split()
                                    n = result[0].split('=')[1]
                                    i = result[1].split('=')[1]
                                    j = result[2].split('=')[1]
                                    link_nodei[n] = i
                                    link_nodej[n] = j
                                else:
                                    break
                            # 单元总数
                            link_total = len(link_nodei)

                            a = SearchKeyword('LINK LOCAL AXES ASSIGNMENTS 1 - TYPICAL', lines)
                            # link局部轴转动字典
                            link_local = {}
                            # 如果没有对link的局部轴进行调整
                            if a == -1:
                                pass
                            else:
                                # 从第a行开始遍历
                                for line in lines[a:]:
                                    # 如果不是空行就一直遍历下去
                                    if not line.isspace():
                                        result = line.split()
                                        link = result[0].split('=')
                                        degree = result[1].split('=')
                                        link_local[link[1]] = degree[1]
                                    else:
                                        break

                            Material = open('Material.tcl', 'a')
                            a = SearchKeyword('LINK PROPERTY DEFINITIONS 04 - DAMPER', lines)
                            if a == -1:
                                pass
                            else:
                                damper = []
                                damper_lib = []
                                damper_mat = []
                                for line in lines[a:]:
                                    # 如果不是空行就一直遍历下去
                                    if not line.isspace():
                                        result = line.split()
                                        name = result[0].split('=')[1]
                                        dof = result[1].split('=')[1]
                                        stiff = result[7].split('=')[1]
                                        dampcoeff = result[8].split('=')[1]
                                        exp = result[9].split('=')[1]
                                        if name not in damper_lib:
                                            damper.append(name)
                                            if dof == 'U1':
                                                damper.append('1')
                                            elif dof == 'U2':
                                                damper.append('2')
                                            elif dof == 'U3':
                                                damper.append('3')
                                            elif dof == 'R1':
                                                damper.append('4')
                                            elif dof == 'R2':
                                                damper.append('5')
                                            else:
                                                damper.append('6')
                                            damper_lib.append(name)
                                        else:
                                            if dof == 'U1':
                                                damper.append('1')
                                            elif dof == 'U2':
                                                damper.append('2')
                                            elif dof == 'U3':
                                                damper.append('3')
                                            elif dof == 'R1':
                                                damper.append('4')
                                            elif dof == 'R2':
                                                damper.append('5')
                                            else:
                                                damper.append('6')
                                            damper_lib.append(name)
                                        mat_total += 1
                                        Material.write('uniaxialMaterial ViscousDamper ' + str(mat_total) + ' ' + stiff + ' ' + dampcoeff + ' ' + exp + '\n')
                                        if name not in damper_mat:
                                            damper_mat.append(name)
                                            damper_mat.append(str(mat_total))
                                        else:
                                            damper_mat.append(str(mat_total))
                                    else:
                                        break
                            # print(damper)
                            # print(damper_lib)
                            # print(damper_mat)

                            a = SearchKeyword('LINK PROPERTY DEFINITIONS 10 - PLASTIC (WEN)', lines)
                            if a == -1:
                                pass
                            else:
                                wen = []
                                wen_lib = []
                                wen_mat = []
                                for line in lines[a:]:
                                    # 如果不是空行就一直遍历下去
                                    if not line.isspace():
                                        result = line.split()
                                        mat_total += 1
                                        # 如果是线性的wen
                                        if result[3].split('=')[1] == 'No':
                                            name = result[0].split('=')[1]
                                            dof = result[1].split('=')[1]
                                            stiff = result[4].split('=')[1]
                                            fy = '0'
                                            ratio = '0'
                                            Material.write('uniaxialMaterial Elastic ' + str(mat_total) + ' ' + stiff + '\n')
                                        else:
                                            name = result[0].split('=')[1]
                                            dof = result[1].split('=')[1]
                                            stiff = result[7].split('=')[1]
                                            fy = result[8].split('=')[1]
                                            ratio = result[9].split('=')[1]
                                            Material.write('uniaxialMaterial Steel01 ' + str(mat_total) + ' ' + fy + ' ' + stiff + ' ' + ratio + '\n')
                                        if name not in wen_lib:
                                            wen.append(name)
                                            if dof == 'U1':
                                                wen.append('1')
                                            elif dof == 'U2':
                                                wen.append('2')
                                            elif dof == 'U3':
                                                wen.append('3')
                                            elif dof == 'R1':
                                                wen.append('4')
                                            elif dof == 'R2':
                                                wen.append('5')
                                            else:
                                                wen.append('6')
                                            wen_lib.append(name)
                                        else:
                                            if dof == 'U1':
                                                wen.append('1')
                                            elif dof == 'U2':
                                                wen.append('2')
                                            elif dof == 'U3':
                                                wen.append('3')
                                            elif dof == 'R1':
                                                wen.append('4')
                                            elif dof == 'R2':
                                                wen.append('5')
                                            else:
                                                wen.append('6')
                                        if name not in wen_mat:
                                            wen_mat.append(name)
                                            wen_mat.append(str(mat_total))
                                        else:
                                            wen_mat.append(str(mat_total))
                                    else:
                                        break
                            # print(wen)
                            # print(wen_lib)
                            # print(wen_mat)
                            Material.close()

                            a = SearchKeyword('LINK PROPERTY ASSIGNMENTS', lines)
                            link_assign = []
                            for line in lines[a:]:
                                # 如果不是空行就一直遍历下去
                                if not line.isspace():
                                    result = line.split()
                                    if result[1].split('=')[1] == '"Plastic':
                                        link = result[0].split('=')[1]
                                        name = result[4].split('=')[1]
                                        link_assign.append(link)
                                        link_assign.append(name)
                                    else:
                                        link = result[0].split('=')[1]
                                        name = result[5].split('=')[1]
                                        link_assign.append(link)
                                        link_assign.append(name)
                                else:
                                    break
                            # print(link_assign)

                            element = open('Element.tcl', 'a')
                            blankspace = ' '
                            # 对单元进行遍历
                            for link in link_nodei.keys():
                                frame_max += 1
                                # 如果link号不在link局部轴转动字典的键列表中
                                if link not in link_local.keys():
                                    # 如果没有定义特殊的局部坐标轴
                                    v_x = LinkVector(link_nodei[link], link_nodej[link])[0]
                                    v_y = LinkVector(link_nodei[link], link_nodej[link])[1]
                                    v_z = LinkVector(link_nodei[link], link_nodej[link])[2]
                                else:
                                    # 如果定义了特殊的局部坐标轴
                                    v_x = LinkVector(link_nodei[link], link_nodej[link], link_local[link])[0]
                                    v_y = LinkVector(link_nodei[link], link_nodej[link], link_local[link])[1]
                                    v_z = LinkVector(link_nodei[link], link_nodej[link], link_local[link])[2]

                                link_name = link_assign[link_assign.index(link) + 1]
                                if link_name in damper_lib:
                                    if damper_lib.index(link_name) == len(damper_lib) - 1:
                                        element.write('element twoNodeLink ' + str(frame_max) + ' ' + link_nodei[link] + ' ' + link_nodej[link] + ' -mat ' + blankspace.join(damper_mat[damper_mat.index(link_name) + 1:])  + ' -dir ' + blankspace.join(damper[damper.index(link_name) + 1:]) + ' -orient ' + str(v_x) + ' ' + str(v_y) + ' ' + str(v_z) + '\n')
                                    else:
                                        link_name_next = damper_lib[damper_lib.index(link_name) + 1]
                                        element.write('element twoNodeLink ' + str(frame_max) + ' ' + link_nodei[link] + ' ' + link_nodej[link] + ' -mat ' + blankspace.join(damper_mat[damper_mat.index(link_name) + 1: damper_mat.index(link_name_next)]) + ' -dir ' + blankspace.join(damper[damper.index(link_name) + 1: damper_mat.index(link_name_next)]) + ' -orient ' + str(v_x) + ' ' + str(v_y) + ' ' + str(v_z) + '\n')
                                else:
                                    if wen_lib.index(link_name) == len(wen_lib) - 1:
                                        element.write('element twoNodeLink ' + str(frame_max) + ' ' + link_nodei[link] + ' ' + link_nodej[link] + ' -mat ' + blankspace.join(wen_mat[wen_mat.index(link_name) + 1:]) + ' -dir ' + blankspace.join(wen[wen.index(link_name) + 1:]) + ' -orient ' + str(v_x) + ' ' + str(v_y) + ' ' + str(v_z) + '\n')
                                    else:
                                        link_name_next = wen_lib[wen_lib.index(link_name) + 1]
                                        element.write('element twoNodeLink ' + str(frame_max) + ' ' + link_nodei[link] + ' ' + link_nodej[link] + ' -mat ' + blankspace.join(wen_mat[wen_mat.index(link_name) + 1: wen_mat.index(link_name_next)]) + ' -dir ' + blankspace.join(wen[wen.index(link_name) + 1: wen_mat.index(link_name_next)]) + ' -orient ' + str(v_x) + ' ' + str(v_y) + ' ' + str(v_z) + '\n')
                                # element twoNodeLink $eleTag $iNode $jNode -mat $matTags -dir $dirs <-orient <$x1 $x2 $x3> $y1 $y2 $y3>
                            element.close()
                            print("Link单元文件已生成    Link File Has Been Created")

                            a = SearchKeyword('JOINT RESTRAINT ASSIGNMENTS', lines)
                            # 由于还未找到opensees中的节点耦合弹簧单元，这里先全部编成fix
                            fix = []
                            if a == -1:
                                pass
                            else:
                                for line in lines[a:]:
                                # 如果不是空行就一直遍历下去
                                    if not line.isspace():
                                        result = line.split()
                                        n = result[0].split('=')[1]
                                        fix.append(n)
                                    else:
                                        break

                            a = SearchKeyword('JOINT SPRING ASSIGNMENTS 2 - COUPLED', lines)
                            # 由于还未找到opensees中的节点耦合弹簧单元，这里先全部编成fix
                            if a == -1:
                                pass
                            else:
                                for line in lines[a::2]:
                                    # 如果不是空行就一直遍历下去
                                    if not line.isspace():
                                        result = line.split()
                                        n = result[0].split('=')[1]
                                        fix.append(n)
                                    else:
                                        break

                            with open('Fix.tcl', 'w') as F:
                                for fi in range(len(fix)):
                                    F.write('fix ' + fix[fi] + ' ' + '1 1 1 1 1 1' + '\n')
                            print("节点边界条件文件已生成    Nodal Boundary File Has Been Created")

