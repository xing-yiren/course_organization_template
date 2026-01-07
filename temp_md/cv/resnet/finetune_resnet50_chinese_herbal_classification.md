<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 0) -->
## **ResNet50中药炮制饮片质量判断**

### **背景介绍**
中药炮制是根据中医药理论，依照临床辨证施治用药的需要和药物自身性质，以及调剂、制剂的不同要求，**将中药材制备成中药饮片所采取的一项制药技术**。平时我们老百姓能接触到的中药，主要指自己回家煎煮或者请医院代煎煮的中药，都是中药饮片，也就是中药炮制这个技术的结果。而中药炮制饮片，大部分涉及到水火的处理，一定需要讲究“程度适中”，炮制火候不够达不到最好药效，炮制火候过度也会丧失药效。

- “生品”一般是指仅仅采用简单净选得到的饮片，通常没有经过火的处理，也是后续用火加工的原料。
- “不及”就是“炮制不到位”，没有达到规定的程度，饮片不能发挥最好的效果。
- “适中”是指炮制程度刚刚好，正是一个最佳的炮制点位，也是通常炮制结束的终点。
- “太过”是指炮制程度过度了，超过了“适中”的最佳状态，这时候的饮片也会丧失药效，不能再使用了。

过去的炮制饮片程度的判断，都是采用的老药工经验判断，但随着老药工人数越来越少，这种经验判断可能存在“失传”的风险。而随着人工智能的发展，使用深度神经网络模型对饮片状态进行判断能达到很好的效果，可以很好的实现经验的“智能化”和经验的传承。

#### **ResNet网络简介**

ResNet50网络是2015年由微软实验室的何恺明提出，获得ILSVRC2015图像分类竞赛第一名。在ResNet网络提出之前，传统的卷积神经网络都是将一系列的卷积层和池化层堆叠得到的，但当网络堆叠到一定深度时，就会出现退化问题。下图是在CIFAR-10数据集上使用56层网络与20层网络训练误差和测试误差图，由图中数据可以看出，56层网络比20层网络训练误差和测试误差更大，随着网络的加深，其误差并没有如预想的一样减小。<br>
<img src="https://mindspore-courses.obs.cn-north-4.myhuaweicloud.com/deep%20learning/AI%2BX/image/image-20230804110559.png" alt="image-20230630102435999" style="zoom:30%;" width="60%" />

ResNet网络提出了残差网络结构(Residual Network)来减轻退化问题，使用ResNet网络可以实现搭建较深的网络结构（突破1000层）。论文中使用ResNet网络在CIFAR-10数据集上的训练误差与测试误差图如下图所示，图中虚线表示训练误差，实线表示测试误差。由图中数据可以看出，ResNet网络层数越深，其训练误差和测试误差越小。<br>
<img src="https://mindspore-courses.obs.cn-north-4.myhuaweicloud.com/deep%20learning/AI%2BX/image/image-20230804110625.png" alt="image-20230630102435999" style="zoom:30%;" width="40%" />

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 1) -->
### **准备阶段**

#### **配置实验环境**

本案例支持在Ascend平台运行：
- 平台：华为启智平台调试任务
- 框架：MindSpore1.8.1/MindSpore2.3.0
- 硬件NPU：Ascend 910

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 2) -->
#### **数据集介绍**

我们使用“中药炮制饮片”数据集，该数据集由成都中医药大学提供，共包含中药炮制饮片的 3 个品种，分别为：蒲黄、山楂、王不留行，每个品种又有着4种炮制状态：生品、不及适中、太过，每类包含 500 张图片共12类5000张图片，图片尺寸为 4K，图片格式为 jpg。
下面是数据集中的一些样例图片：

<img src="https://mindspore-courses.obs.cn-north-4.myhuaweicloud.com/deep%20learning/AI%2BX/image/image-20230508160428881.png" alt="image-20230630102435999" style="zoom:67%;" width="90%"/>

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 3) -->
#### **准备数据**

我们使用的数据集在调试任务中配置加载，并修改代码中对应url链接。

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 4) -->
#### **数据预处理**

原图片尺寸为4k比较大，我们预处理将图片resize到指定尺寸。

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 5) -->
#### **数据集划分**

数据集已划分为训练集和测试集，可以接着继续划分验证集。

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 6) -->
#### **定义数据加载方式**

通过重写Iterable类的方式加载图片数据集，支持单张图片和文件夹进行加载。

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 7) -->
#### **加载数据**

对数据集使用定义好的方式进行加载。

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 8) -->
#### **类别标签说明**

由于平台字体问题，无法正确显示中文，这里给出英文标签对应的类别：
- ph-sp：蒲黄-生品
- ph_bj：蒲黄-不及
- ph_sz：蒲黄-适中
- ph_tg：蒲黄-太过
- sz_sp：山楂-生品
- sz_bj：山楂-不及
- sz_sz：山楂-适中
- sz_tg：山楂-太过
- wblx_sp：王不留行-生品
- wblx_bj：王不留行-不及
- wblx_sz：王不留行-适中
- wblx_tg：王不留行-太过

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 9) -->
#### **数据可视化展示**

对已经加载好的数据集，选取部分数据展示。

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 10) -->
### **创建分类网络**

当处理完数据后，就可以来进行网络的搭建了。我们使用经典的Resnet50作为基础模型，模型由MindSpore框架编写，我们在此基础上进行了修改，将最后一层的输出改为类别数12，以适应我们的数据集。

#### **模型结构展示**

<img src="https://mindspore-courses.obs.cn-north-4.myhuaweicloud.com/deep%20learning/AI%2BX/image/image-20230630095910087.png" alt="image-20230630095910087" style="zoom:80%;" />

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 11) -->
#### **构建残差网络结构**

残差结构是ResNet网络中最重要的结构，其结构图如下图所示，残差网络由两个分支构成：一个主分支，一个shortcuts（图中弧线表示）。主分支通过堆叠一系列的卷积操作得到，shortcuts从输入直接到输出，主分支的输出与shortcuts的输出相加后通过Relu激活函数后即为残差网络最后的输出。<br>
<img src="https://mindspore-courses.obs.cn-north-4.myhuaweicloud.com/deep%20learning/AI%2BX/image/image-20230804113155.png" alt="image-20230630102435999" style="zoom:67%;" width="40%"/>

残差网络结构主要由两种，一种是Building Block，适用于较浅的ResNet网络，如ResNet18和ResNet34；另一种是Bottleneck，适用于层数较深的ResNet网络，如ResNet50、ResNet101和ResNet152。

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 12) -->
#### **定义 Building Block**

Building Block结构图如下图所示，主分支有两层卷积网络结构：

- 主分支第一层网络以输入channel为64为例，首先通过一个3×3的卷积层，然后通过Batch Normalization层，最后通过Relu激活函数层，输出channel为64；

- 主分支第二层网络的输入channel为64，首先通过一个3×3的卷积层，然后通过Batch Normalization层，输出channel为64。

最后将主分支输出的特征矩阵与shortcuts输出的特征矩阵相加，通过Relu激活函数即为Building Block最后的输出。<br>
<img src="https://mindspore-courses.obs.cn-north-4.myhuaweicloud.com/deep%20learning/AI%2BX/image/image-20230804114627.png" alt="image-20230630102435999" style="zoom:67%;" width="30%" />

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 13) -->
#### **定义 Bottleneck**

Bottleneck结构图如下图所示，在输入相同的情况下Bottleneck结构相对Building Block结构的参数数量更少，更适合层数较深的网络，ResNet50使用的残差结构就是Bottleneck。该结构的主分支有三层卷积结构，分别为1×1的卷积层、3×3卷积层和
1×1的卷积层，其中1×1的卷积层分别起降维和升维的作用。
- 主分支第一层网络以输入channel为256为例，首先通过数量为64，大小为的卷积核进行降维，然后通过Batch Normalization层，最后通过Relu激活函数层，其输出channel为64；
- 主分支第二层网络通过数量为64，大小为的卷积核提取特征，然后通过Batch Normalization层，最后通过Relu激活函数层，其输出channel为64；
- 主分支第三层通过数量为256，大小的卷积核进行升维，然后通过Batch Normalization层，其输出channel为256。

最后将主分支输出的特征矩阵与shortcuts输出的特征矩阵相加，通过Relu激活函数即为Bottleneck最后的输出。<br>
<img src="https://mindspore-courses.obs.cn-north-4.myhuaweicloud.com/deep%20learning/AI%2BX/image/image-20230804115129.png" alt="image-20230630102435999" style="zoom:67%;" width="30%"/>

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 14) -->
#### **构建ResNet网络**

ResNet网络由基本的Building Block/Bottleneck块堆叠而成，我们将重复的结构定义为残差网络块。

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 15) -->
#### **ResNet分类模型初始化**

模型定义完成后，实例化ResNet分类模型

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 16) -->
### **模型训练**

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 17) -->
#### **定义训练参数**

我们设置epoch为50,Momentum作为优化器，其中参数momentum设为0.9，而损失函数则采用SoftmaxCrossEntropyWithLogits。

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 18) -->
#### **定义训练推理函数**

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 19) -->
#### **开始训练**

在每个训练轮次中，使用训练集进行模型训练，并计算交叉熵损失以更新参数。随后在验证集上对模型进行测试，并以"accuracy"作为评价指标来评估模型的性能。为了防止过拟合，我们引入了早停机制，通过监控验证集上的指标，及时停止训练以避免过拟合，并保存具有最佳性能的模型参数。通过这样的训练过程，我们期望模型能够逐渐优化，并达到更好的性能水平。

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 20) -->
#### **结果可视化展示**

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 21) -->
### **模型推理**

在模型推理阶段，我们提供了两种预测推理方式：单张图片推理和数据集推理方式

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 22) -->
#### **加载模型**

首先加载训练好了的最佳模型权重。

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 23) -->
#### **通过传入图片路径进行推理**

给定单张图片的路径推理预测分类结果

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 24) -->
#### **通过传入测试数据集进行推理**

直接给定测试数据集，模型将对数据集中的样本进行预测，并生成可视化展示来呈现推理结果。

<!-- ORIGIN: cv/resnet/finetune_resnet50_chinese_herbal_classification.ipynb (cell: 25) -->
### **参考文献**

[1] He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for image recognition. In Proceedings of the IEEE conference on computer vision and pattern recognition (pp. 770-778).


