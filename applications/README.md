<div align=center>
  <h1>基于昇思+香橙派开发板的应用实践案例</h1>
</div>


本路径下汇总了基于 昇思MindSpore 的香橙派开发板应用案例，覆盖带框架推理、离线推理两大场景，包含图像、文本、表格、视频等多模态任务。

## 📢 最新消息

- 2025-12-18 [功能优化]：重构仓库结构以优化应用导航体验；新增Issue与PR模板，让贡献流程更标准化。

## 前置知识

在进行实践之前，您需要掌握：

- Python基础
- Linux命令基础
- Jupyter基础

## 环境准备

在开发前，请确保环境中的各软件包版本已完成配套，详见[环境搭建指南](https://www.mindspore.cn/tutorials/zh-CN/r2.7.1/orange_pi/environment_setup.html)

## 案例清单

应用案例（通常以 Notebooks 形式呈现）按技术领域分类，各领域下再按模型进一步细分，为开发者提供清晰的索引导航。

| 分类     | 描述                           |
| :------ | :----------------------------- |
| [online](./online/) | 带框架（MindSpore）的训练、推理案例，包含官方开发案例和社区开发者贡献案例。 |
| [offline](./offline/) | 离线推理（OM推理或MindIR推理）案例，包含官方开发案例和社区开发者贡献案例。|

## 版本维护

各应用案例配套的 CANN 版本、MindSpore 版本、MindSpore 套件版本及开发板型号，均已在对应目录的`README`文件和案例中明确说明。若开发者希望将特定案例升级至新版本，可提交[Issue](https://github.com/mindspore-lab/orange-pi-mindspore/issues)并注明目标 MindSpore 版本。

> 我们同样诚挚欢迎开发者更新、完善或优化案例，通过提交[Pull Request](https://github.com/mindspore-lab/orange-pi-mindspore/pulls)贡献至社区，携手共建昇思 + 香橙派开发板生态！

## 常见问题（FAQ）

详见Wiki中[FAQ](https://github.com/mindspore-lab/orange-pi-mindspore/wiki/Developer-FAQ)。

## 贡献与反馈

1. **Issue**：欢迎各位开发者通过 [Issue](https://github.com/mindspore-lab/orange-pi-mindspore/issues) 提交建议或 bug 反馈

2. **Pull Request**: 开发者可发起 [PR](https://github.com/mindspore-courses/applications/pulls) 进行Bug修复或代码贡献（提交前请参考[提交规范](https://github.com/mindspore-lab/orange-pi-mindspore/wiki/Contributing-Guidelines)，由Committer @xing-yiren 及另一位Committer 完成评审合入），你的每一份参与都能让本项目更加完善。

3. **开源项目**：若开发者有符合条件的开源项目推荐/自荐，欢迎按照[项目仓规范](https://github.com/mindspore-lab/orange-pi-mindspore/wiki/Contributing-Guidelines)完善项目内容后，邮件至contact@public.mindspore.cn进行投稿，邮件标题请参考：`【昇思+香橙派项目投稿】项目名称`格式，并在正文中对项目进行简单介绍，附上代码仓链接。

### 提交规范

详见WIKI：[Issue与PR提交规范](https://github.com/mindspore-lab/orange-pi-mindspore/wiki/Contributing-Guidelines)

### 贡献者展示

向本项目的贡献者们致以最诚挚的感谢！

<div align=center style="margin-top: 30px;">
  <a href="https://github.com/mindspore-lab/orange-pi-mindspore/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=mindspore-lab/orange-pi-mindspore" />
  </a>
</div>
