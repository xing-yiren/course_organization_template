## Docker镜像

为方便开发者更加便捷地进行代码实践，节约环境准备的时间，我们提供了预装好的基础Dockerfile文件。课程的所有镜像可从[dockerfile](./dockerfile/)。本课程镜像文件信息如下，开发者可根据实际需求进行拉取：

| 硬件平台 | 镜像名称        | 标签      |  说明                     | Dockerfile文件 |
| :------ | :-------------- | :------- | :------------------------ | :------------- |
| CPU     | xxx             | xxx      | xxx                       | xxx            |
| GPU     | xxx             | xxx      | xxx                       | xxx            |
| NPU     | xxx             | xxx      | xxx                       | xxx            |

### Docker镜像使用

- CPU
    1. 进入Dockfile所在目录

        ```bash
        cd dockerfile/cpu
        ```

    2. 镜像构建

        ```bash
        docker build -t [镜像名称:标签] .  
        ```

    3. 构建完成后，通过以下命令查看镜像：

        ```bash
        docker images | grep [镜像名称]  
        ```
        若输出类似以下内容，说明构建成功：
        ```text
        [镜像名称]   [镜像标签]     abc12345   2 minutes ago   XXGB  
        ```

    4. 启动容器

        ```bash
        docker run -it [镜像名称:标签] /bin/bash
        ```

    5. 检查容器是否已启动

        ```bash
        docker ps
        ```
    
        若输出类似以下内容，说明启动成功：

        ```text
        CONTAINER ID   NAMES        STATUS  
        123abc        [镜像名称]  Up 5 minutes
        ```

    6. 进入容器

        ```bash
        docker exec -it [容器ID或名称] /bin/bash  
        ```

- GPU

    1. 进入Dockfile所在目录

        ```bash
        cd dockerfile/gpu
        ```

    2. 镜像构建

        ```bash
        docker build -t [镜像名称:标签] .  
        ```

    3. 构建完成后，通过以下命令查看镜像：

        ```bash
        docker images | grep [镜像名称]  
        ```

        若输出类似以下内容，说明构建成功：
    
        ```text
        [镜像名称]   [镜像标签]     abc12345   2 minutes ago   XXGB
        ```

    4. 启动容器

        ```bash
        docker run -it [镜像名称:标签] -v xxx --runtime=nvidida /bin/bash
        ```

    5. 检查容器是否已启动

        ```bash
        docker ps
        ```

        若输出类似以下内容，说明启动成功：

        ```text
        CONTAINER ID   NAMES        STATUS  
        123abc        [镜像名称]  Up 5 minutes
        ```

    6. 进入容器

        ```bash
        docker exec -it [容器ID或名称] /bin/bash  
        ```

- NPU

    1. 进入Dockfile所在目录

        ```bash
        cd dockerfile/gpu
        ```

    2. 镜像构建

        ```bash
        docker build -t [镜像名称:标签] .  
        ```

    3. 构建完成后，通过以下命令查看镜像：

        ```bash
        docker images | grep [镜像名称]  
        ```

        若输出类似以下内容，说明构建成功：

        ```text
        [镜像名称]   [镜像标签]     abc12345   2 minutes ago   XXGB
        ```

    4. 启动容器

        ```bash
        docker run -it \  
            -v $(pwd):/workspace \  # 挂载工作目录（根据需求修改）  
            --device /dev/davinci0 \  
            --device /dev/davinci1 \  
            --device /dev/davinci2 \  
            --device /dev/davinci3 \  
            --device /dev/davinci_manager \  
            --device /dev/devmm_svm \  
            --device /dev/hisi_hdc \  
            -e ASCEND_VISIBLE_DEVICES=0,1,2,3 \  # 关联NPU设备  
            -e LD_LIBRARY_PATH=/usr/local/Ascend/lib:$LD_LIBRARY_PATH \  
            [镜像名称:标签] \  # 替换为实际镜像名:标签  
            /bin/bash  
        ```

    5. 检查容器是否已启动

        ```bash
        docker ps
        ```

        若输出类似以下内容，说明启动成功：

        ```text
        CONTAINER ID   NAMES        STATUS  
        123abc        [镜像名称]  Up 5 minutes
        ```

    6. 进入容器

        ```bash
        docker exec -it [容器ID或名称] /bin/bash  
        ```

### Docker镜像测试

如希望测试Docker是否正常工作，可运行如下Python代码并检查输出：

```python
# mindspore及相关套件 测试
```
