import pika
from taobaolive_spider.config import environments


def push_task(queue_name, routing_key, body, env='dev'):
    env_dict = environments.get(env)
    # 连接RabbitMq 默认端口5672
    connection = pika.BlockingConnection(pika.ConnectionParameters(env_dict.get('mq_host'), env_dict.get('mq_port')))

    # 订阅一个频道
    channel = connection.channel()

    # 声明一个叫hello的队列
    channel.queue_declare(queue=queue_name, durable=True)

    # 消息不会直接发送到队列，先发送到交换机，exchange为空，默认交换--->允许我们准确的指定到那一个队列中，routing_key表示队列名称，body代表要发送过去的消息
    channel.basic_publish(exchange='', routing_key=routing_key, body=body, properties=pika.BasicProperties(delivery_mode=2))

    # 刷新网络缓冲区，连接断开
    connection.close()


if __name__ == '__main__':
    push_task('test', 'test', '123')