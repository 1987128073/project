import pika
from taobaolive_spider.config import environments


class ConsumingMsg(object):

    def __init__(self, queue_name, env, func=None,):
        self.env_dict = environments.get(env)
        self.func = func
        # 连接RabbitMq
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.env_dict.get('mq_host'), self.env_dict.get('mq_port')))

        # 订阅一个频道
        self.channel = self.connection.channel()

        # 确保队列存在，多次运行也只会创建一个,如果先运行接收队列的py文件，没有声明这个队列会报错。可以让它一直等待发送方发送消息。
        self.channel.queue_declare(queue=queue_name, durable=True)

        # 指定接收名为hello的队列， no_ack接收到后不发确认信息回去
        self.channel.basic_consume(queue_name, self.callback)

    # 接收到hello后执行的回调函数
    def callback(self, ch, method, propertites, body):
        msg = body.decode('utf-8')
        print(" [x] Received {}".format(msg))
        if self.func is not None:
            self.func(msg)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consuming_task(self):
        # 消费者开始
        self.channel.start_consuming()


if __name__ == '__main__':
    cm = ConsumingMsg(queue_name='test', env='dev')
    cm.consuming_task()