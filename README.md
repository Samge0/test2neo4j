## text2neo4j
Text2Neo4j 是一个遍历文档、从文本中提取关系并将其保存到 Neo4j 数据库中以形成知识图谱的工具。本项目结合了 Dify 和 LLaMA3.1（8B 模型）来高效处理和提取复杂关系。

本工具主要的流程为：遍历目录-》读取文本-》对文本进行关系提取-》写入neo4j数据库（图谱）


### 功能特性
- 目录遍历： 自动遍历目录以定位并读取文本文件。
- 关系提取： 利用开元 AI 模型从文本中提取有意义的关系。
- Neo4j 集成： 将提取的关系直接写入 Neo4j 数据库，创建一个可查询的知识图谱。


### 创建env环境
```shell
conda create -n test2neo4j python=3.10.13 -y
```

### 安装依赖
```shell
pip install -r requirements.txt
```

### 下载文档
```shell
python parses/main.py
```

### 其他说明
llama3.1:8b模型的上下文支持128k，适合处理比较长的文本。

目前从文本中提取关系的方式依赖[Dify](https://github.com/langgenius/dify)+[llanma3.1:8b](https://ollama.com/library/llama3.1)的组合，理论上来说，单纯的使用`llanma3.1:8b`也可以提取关系，主要都是调整适当的`prompt`罢了。

建议使用`Dify`+`llanma3.1:8b`，因为本项目脚本默认基于此组合完成，其他的关系提取方式可自行尝试。

以下是关系提取的`prompt`：

<details> <summary>点击展开查看prompt信息 >></summary>

```text
"你将扮演一个智能助手的角色，专注于从给定的文本输入中提取所有潜在的关系。请确保遵循以下要求和输出格式：
目标： 从输入文本中识别并提取广泛的实体和实体之间的各种关系，包括但不限于人物关系、地理关联、职业经历、教育背景等。
输出格式： 你的输出必须是一个JSON对象，结构应包括：
entities: 一个数组，包含所有提取的实体对象，每个实体应包含 name (实体名称) 和 type (实体类型)。
relationships: 一个数组，包含所有提取的关系对象，每个关系应包含 source (关系的起点实体)，target (关系的终点实体)，type (关系类型)，以及可选的 date (表示关系发生的日期)。
示例输出：
json

{
  "entities": [
    { "name": "高捷", "type": "Person" },
    { "name": "江苏", "type": "Location" },
    { "name": "东南大学", "type": "Organization" },
    { "name": "本科", "type": "Degree" }
  ],
  "relationships": [
    { "source": "高捷", "target": "江苏", "type": "hometown" },
    { "source": "高捷", "target": "东南大学", "type": "alumnus" },
    { "source": "高捷", "target": "本科", "type": "degree" }
  ]
}

约束：
你的回答必须严格符合上述JSON格式。
每个实体和关系都应该是从输入中直接推断出来的。
若没有关系可提取，relationships 数组应为空。
对于存在的日期信息，确保准确提取并以 "YYYY-MM-DD" 格式返回。
确保每个 type 都是单个单词，不包含空格且不包含-。
请确保输出JSON是有效的，不包含任何语法错误或不完整的内容。
广泛覆盖：
尽可能识别多种类型的关系，如亲属关系、地理关联、教育经历、职业背景、时间相关性、以及任何可识别的连接。
对于描述或暗示的关系，不要遗漏，务必详细标明关系类型。
示例输入：
"高捷，祖籍江苏，本科毕业于东南大学。"
注意事项：
确保实体类型精确，尽可能使用标准化的类型标签 (如 Person, Organization, Location, Date, Degree, Event 等)。
对于复杂的关系，请明确描述关系类型，以便清晰传达关系的性质。
当存在模糊或隐含的关系时，尝试以合理的推断方式提取可能的关系。
请根据上述规范返回结果。"
```

</details>


### 测试数据&测试结果
- 测试数据1：

    ```text
    高捷，祖籍江苏，本科毕业于东南大学。
    ```

    <details> <summary>点击查看测试数据1的返回结果 >></summary>

    ```json
    {
        "entities": [
            {
                "name": "高捷",
                "type": "Person"
            },
            {
                "name": "江苏",
                "type": "Location"
            },
            {
                "name": "东南大学",
                "type": "Organization"
            },
            {
                "name": "本科",
                "type": "Degree"
            }
        ],
        "relationships": [
            {
                "source": "高捷",
                "target": "江苏",
                "type": "hometown"
            },
            {
                "source": "高捷",
                "target": "东南大学",
                "type": "alumnus",
                "date": null
            },
            {
                "source": "高捷",
                "target": "本科",
                "type": "degree"
            }
        ]
    }
    ```

    </details>


- 测试数据 2：

    ```text
    2024年8月26日，公司A的陈总与公司B的刘总达成合作协议。陈总来自贵州，于2000年毕业于北京大学。刘总来自四川，于2005年毕业于深圳大学。
    ```

    <details> <summary>点击查看测试数据2的返回结果 >></summary>

    ```json
    {
        "entities": [
            {
                "name": "陈总",
                "type": "Person"
            },
            {
                "name": "公司A",
                "type": "Organization"
            },
            {
                "name": "公司B",
                "type": "Organization"
            },
            {
                "name": "刘总",
                "type": "Person"
            },
            {
                "name": "贵州",
                "type": "Location"
            },
            {
                "name": "北京大学",
                "type": "Organization"
            },
            {
                "name": "四川",
                "type": "Location"
            },
            {
                "name": "深圳大学",
                "type": "Organization"
            },
            {
                "name": "2000年",
                "type": "Date"
            },
            {
                "name": "2005年",
                "type": "Date"
            }
        ],
        "relationships": [
            {
                "source": "陈总",
                "target": "公司A",
                "type": "CEO"
            },
            {
                "source": "刘总",
                "target": "公司B",
                "type": "CEO"
            },
            {
                "source": "陈总",
                "target": "贵州",
                "type": "hometown"
            },
            {
                "source": "陈总",
                "target": "北京大学",
                "type": "alumnus"
            },
            {
                "date": "2000年",
                "source": "陈总",
                "target": "北京大学",
                "type": "graduation"
            },
            {
                "source": "刘总",
                "target": "四川",
                "type": "hometown"
            },
            {
                "source": "刘总",
                "target": "深圳大学",
                "type": "alumnus"
            },
            {
                "date": "2005年",
                "source": "刘总",
                "target": "深圳大学",
                "type": "graduation"
            },
            {
                "source": "陈总",
                "target": "公司B",
                "type": "partner"
            },
            {
                "source": "刘总",
                "target": "公司A",
                "type": "partner"
            }
        ]
    }
    ```

</details>

### 相关截图
![image](https://github.com/user-attachments/assets/f9c9356f-3e8f-489c-a25e-029766f5351c)
![image](https://github.com/user-attachments/assets/fea23358-b3a0-402b-a505-2daa0c0d8a4e)
![image](https://github.com/user-attachments/assets/8180d018-388f-414e-bb76-f5ddf0fc12ab)
![image](https://github.com/user-attachments/assets/246bc635-1c42-4cde-81f1-5827666057aa)

### 已知问题
由于使用 LLaMA3.1:8B 模型从文本中提取关系，每次提取的关系数量和类型可能会有所不同。如果需要更精准的关系提取，可以尝试调整 prompt 或选择更适合的模型进行优化和调试。

