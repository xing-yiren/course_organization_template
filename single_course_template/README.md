<div align=center>
  <h1>课程名称</h1>
</div>


（1-2句话点名项目核心价值）本项目是一个围绕XXX技术领域，针对XXX学习群体的实践课程，提供理论知识课件、实践代码，覆盖从数据处理、模型构建、模型训练、模型评估、模型推理的全流程实践。如开发者对教程有任何问题或修改建议，欢迎提交[issue](issue链接)和[pull request](PR链接)。

### 📢 最新消息
- 2025-10-21 「课程更新」：新增XXX课程，包含完整视频、课件及代码案例。（[查看详情](xxxx)）
- 2025-10-18 「功能优化」：项目仓完成重构，查找课程资源更清晰，新增PR检查门禁，合入内容更规范。（[查看详情](xxx)）
- 2025-10-10 「Bug修复」：修复xxxxxx问题，感谢@username的PR贡献。（[查看详情](xxxx)）

## 目录

- [课程定位与适用人群](#课程定位与适用人群)
- [前置知识](#前置知识)
- [算力平台与Docker镜像](#算力平台与Docker镜像)
    - [算力平台](#算力平台)
    - [Docker镜像](#docker镜像)
- [快速入门](#快速入门)
- [课程内容](#课程内容)
    - [课程清单](#课程清单)
    - [基于本课程的三方实践清单](#基于本课程的三方实践清单)
- [版本维护](#版本维护)
    - [版本维护策略](#版本维护策略)
    - [现有版本维护状态](#现有版本维护状态)
- [贡献与反馈](#贡献与反馈)
    - [Issue提交规范](#issue提交规范)
    - [PR提交规范](#pr规范)
    - [贡献者展示](#贡献者展示)
- [常见问题（FAQ）](#常见问题faq)

## 课程定位与适用人群

- **课程定位**：课程核心目标，如从零掌握基于昇思MindSpore的深度学习基础实践
- **适用人群**：适用学习群体，如初接触AI的开发者

## 前置知识

在学习本门课程之前，您需要掌握：
- Python基础
- Linux命令基础
- Jupyter基础
- 包管理工具（如pip、conda等）
- Docker镜像使用
- 关联其他课程代码仓

## 算力平台与Docker镜像

### 算力平台
本项目支持在CPU/GPU/NPU（根据实际情况进行删减）上运行，[昇思大模型平台](https://xihe.mindspore.cn/)提供免费NPU算力，平台基础使用可参考[本教程](https://docs.xihe.mindspore.cn/zh/tutorial/jupyter/)。

### Docker镜像
为方便开发者更加便捷地进行代码实践，节约环境准备的时间，我们提供了预装好的基础Docker镜像。课程的所有镜像已托管在[XXX平台](Docker平台链接)上。本课程推荐使用镜像如下：

| 硬件平台 | Docker镜像仓库  | 标签      |  说明                     |
| :------ | :-------------- | :------- | :------------------------ |
| CPU     | xxx             | xxx      | xxx                       |
| GPU     | xxx             | xxx      | xxx                       |
| NPU     | xxx             | xxx      | xxx                       |

镜像基础使用和测试教程详见：[Docker镜像使用](../README.md#docker镜像使用)

## 快速入门

本章节将以一个较为简单的实践为例，讲解在进入编程环境后，如何完成从仓库克隆-环境准备-代码运行-结果展示的完整实践体验流程，其他课节的实践部分可参考本章节操作指导。

1. 仓库克隆

    ```bash
    git clone https://github.com/mindspore-courses/xxx.git
    cd xxx
    ```

2. 环境准备

    ```bash
    # 如果仅需pip install即可完成
    pip install -r requirements.txt
    # 如果需要其他操作
    python setup.py
    ```

3. 代码运行

- Python脚本文件

    ```bash
    cd 01_xxx
    # input_dir: 输入数据集路径
    # output_dir：输出保存路径
    python xxx.py --input_dir xxx --output_dir xxx
    ```

- Jupyter Notebook文件

    选择`01_xxx`文件夹，点击xxx.ipynb文件。

    ![查看jupyter文件](./images/xxxx)

    选择kernel后，可点击代码块左侧的运行图标执行代码。

    ![代码块运行](./images/xxx)

4. 结果展示

    ![结果展示](./images/xxx)

## 课程内容

### 课程清单

| 阶段划分 | 序号 | 课节    | 简介             | 课程资源 | 能力认证入口 | 
| :------ | :-- | :------ | :--------------- | :------- | :--------- |
| 第一阶段 | 1   | xxx     | xxx              | [PPT](跳转链接) · [代码](跳转链接) · [视频](跳转链接) |  |
|         | 2   | xxx     | xxx              | [PPT](跳转链接) · [代码](跳转链接) · [视频](跳转链接) | [第一阶段认证入口](xxxx) |
| 第二阶段 | 3   | xxx     | xxx              | [PPT](跳转链接) · [代码](跳转链接) · [视频](跳转链接) |  |
|         | 4   | xxx     | xxx              | [PPT](跳转链接) · [代码](跳转链接) · [视频](跳转链接) | [第二阶段认证入口](xxxx) |
### 基于本课程的三方实践清单

| 序号 | 模型    | 简介             | 代码 | 作者 |
| :-- | :------ | :--------------- | :-- | :-- |
| 1   | xxx     | xxx              | [Link](跳转链接) | xxx |

## 版本维护

### 版本维护策略

项目随昇思MindSpore及昇思MindSpore套件迭代同步发布版本，分以下几种维护阶段。

| **状态**    | **持续时间**   | **说明**                                         |
|-------------|---------------|-------------------------------------------------|
| Planning    | 1 - 3 months  | 特性规划。                                       |
| Development | 3 months      | 特性开发。                                       |
| Maintained  | 6 - 12 months | 允许所有问题修复的合入，并发布版本。                |
| Unmaintained| 0 - 3 months  | 允许所有问题修复的合入，无专人维护，不再发布版本。   |
| End Of Life (EOL) |  N/A |  不再接受修改合入该版本。          |

### 现有版本维护状态

| 版本名 | 当前状态     | CANN toolkit/kernel | MindSpore | MindSpore NLP |
| :----- |:----------- |:------ |:------ | :----- |
| master | Development | xxx    | xxx    | xxx    |
| r1.0   | Maintained  | xxx    | xxx    | xxx    |

## 常见问题（FAQ）
- 问题1：xxx
    - 解答：xxx

## 贡献与反馈

欢迎各位开发者通过 Issue 提交建议或 bug 反馈，也可直接发起 PR 进行Bug修复或代码贡献（提交前请参考仓库贡献规范，由Committer @username 完成评审合入），你的每一份参与都能让本项目更加完善。

### Issue提交规范
详见[Issue提交规范](https://github.com/mindspore-courses/.github/README.md#issue提交规范)

### PR提交规范
详见[PR提交规范](https://github.com/mindspore-courses/.github/README.md#pr提交规范)

### 贡献者展示

向本项目的贡献者们致以最诚挚的感谢！

<div align=center style="margin-top: 30px;">
  <a href="https://github.com/mindspore-courses/xxx/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=mindspore-courses/xxx" />
  </a>
</div>

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=mindspore-courses/xxx&type=Date)](https://star-history.com/#mindspore-courses/xxx&Date)