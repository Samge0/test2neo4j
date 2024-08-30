#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author：samge
# date：2024-08-30 17:39
# describe：处理neo4j图谱数据

from neo4j import GraphDatabase

from parses import configs

# Neo4j 数据库
driver = None

def get_driver():
    """
    Get the Neo4j database driver.

    If the driver is not yet created, create it with the given config values.

    :return: The Neo4j database driver
    """
    global driver
    if driver is None:
        driver = GraphDatabase.driver(configs.NEO4J_URL, auth=(configs.NEO4J_USER, configs.NEO4J_PASSWORD))
    return driver

def close_driver():
    """
    Close the Neo4j driver.

    This method is used to explicitly close the driver. If the driver is not yet created, this method does nothing.

    :return: None
    """
    global driver
    if driver is not None:
        driver.close()  

def import_to_neo4j(data):
    if not data: return
    with get_driver().session() as session:
        # 创建节点
        for entity in data["entities"]:
            entity['type'] = entity['type'].lower().replace(' ', '_').replace('-', '_')
            session.write_transaction(create_node, entity)

        # 创建关系
        for relationship in data["relationships"]:
            entity['type'] = entity['type'].lower().replace(' ', '_').replace('-', '_')
            session.write_transaction(create_relationship, relationship)

def create_node(tx, entity):
    query = f"""
    MERGE (n:{entity['type']} {{name: $name}})
    """
    tx.run(query, name=entity['name'])

def create_relationship(tx, relationship):
    query = f"""
    MATCH (a {{name: $source}})
    MATCH (b {{name: $target}})
    MERGE (a)-[r:{relationship['type'].upper()}]->(b)
    """
    tx.run(query, source=relationship['source'], target=relationship['target'])


if __name__ == "__main__":
    # 示例数据
    data = {
        "entities": [
            { "name": "徐院", "type": "Person" },
            { "name": "前瞻产业研究院", "type": "Organization" },
            { "name": "加州大学伯克利分校", "type": "Organization" },
            { "name": "俄罗斯工程院", "type": "Organization" },
        ],
        "relationships": [
            { "source": "前瞻产业研究院", "target": "徐院", "type": "employer" },
            { "source": "加州大学伯克利分校", "target": "徐院", "type": "almaMater" },
            { "source": "俄罗斯工程院", "target": "徐院", "type": "affiliate" },
        ]
    }
    
    # 导入数据
    import_to_neo4j(data)
    
    # 关闭数据库连接
    close_driver()
    
    print("all done")