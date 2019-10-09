import hashlib


def makesign(secret, parameters):
    # ===========================================================================
    # '''淘宝开发者平台签名方法
    # @param secret: 签名需要的密钥
    # @param parameters: 支持字典和string两种
    # '''
    # ===========================================================================
    # 如果parameters 是字典类的话
    if hasattr(parameters, "items"):
        ks = parameters.keys()
        keys = list(ks)
        keys.sort()
        parameters = "%s%s%s" % (secret,
                                 str().join('%s%s' % (key, parameters[key]) for key in keys),
                                 secret)
        m = hashlib.md5()
        m.update(parameters.encode(encoding='utf-8'))
        return m.hexdigest().upper()
