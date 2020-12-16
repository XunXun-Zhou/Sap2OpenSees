# Sap2Opensees

    作者：周迅
    邮箱：702135971@qq.com
    语言：python 3.8.5

    这段代码实现了由Sap2000至OpenSees的数据传递，目前已经对桥梁结构Sap模型进行了测试与优化。  
    请先在Sap2000中建立好有限元模型，并以s2k文件格式导出，再通过这段代码就可以转成tcl文件。
    程序将继续开发及优化，敬请期待。有任何问题可与我联系。
    
    Author: Zhou Xun
    Email: 702135971@qq.com
    language: python 3.8.5

    This code implements data transmission from Sap2000 to OpenSees, which has been tested and optimized for BRIDGES.
    You can model your bridge in Sap2000, then export it in s2k format.
    Automatically transmission to tcl files will be done by this code.
    The program will continue to be developed and optimized, please stay tuned.
    Please feel free to contact me if you have any questions.

## 注意点 Notes
    
    由于时间紧促，在程序编译过程中对一些问题进行了简化，并且由于建模习惯的不同，不可避免会遗漏一些细节，其中至少包括
    
    1、未考虑恒载作用下梁柱单元的内力；
    2、link单元暂时仅支持damper、wen两种类型；
    3、暂时未找到OpenSees中耦合节点弹簧单元，因此所有土弹簧都直接采用固接；
    4、缆索单元的初始内力采用了初应变模拟，其准确度有待考证;
    5、节点质量直接采用Sap2000中计算得到的结果，因此需要先跑一下模态分析。


    Due to time, some issues were simplified during program compilation.
    Meanwhile, some details will inevitably be missed for different modeling habits, including
    
     1. The internal force of beam-column element under dead load is not considered;
     2. The link element only supports two types: damper and wen;
     3. The coupled nodal spring element has not been found(developed?) yet in OpenSees, so all boundaries are directly fixed;
     4. The initial internal force of the cable element is simulated by its initial strain, whose accuracy needs to be verified.
     5. The nodal mass is calculated by SAP2000, so it is necessary to run modal analysis first.
    
