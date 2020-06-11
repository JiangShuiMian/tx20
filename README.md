## 项目结构

#### 1、cfgs
    
- 所以配置文件，路径等都从这里拿


#### 2、datas

- 所有数据文件，包括原始数据，清理后的数据等

#### 3、dc

- data center 数据中心, 数据探索，清理，转换，准备训练数据等


#### 4、docs 

- 相关文档

#### 5、GraphSage算法

- GraphSage算法的开源实现

#### 6、logs 

- 所有日志

- 0611 - 1
w2v从32维改为64维
age: Full validation stats: loss= 1.48301 f1_micro= 0.38917 f1_macro= 0.35781 time= 214.86323
gender:Full validation stats: loss= 0.19691 f1_micro= 0.92629 f1_macro= 0.91741 time= 247.27234

- 0611 - 2

    - 改进

        w2v从64维改为128维， 迭代次数增加到10

    - 结果

        age: Full validation stats: loss= 1.45712 f1_micro= 0.39890 f1_macro= 0.37079 time= 185.53061
        gender:Full validation stats: loss= 0.19017 f1_micro= 0.93052 f1_macro= 0.92091