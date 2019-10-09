import frida, sys
jscode = """
Java.perform(function(){
var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.isGlobalSpdySwitchOpen.overload().implementation = function(){
        var ret = this.isGlobalSpdySwitchOpen.apply(this, arguments);
        console.log("isGlobalSpdySwitchOpenl "+ret)        
        return false
    }
 
});
"""

def on_message(message, data):
    if message['type'] == 'send':
        print(" {0}".format(message['payload']))
    else:
        print(message)
 
process = frida.get_usb_device().attach('com.taobao.taobao')
script = process.create_script(jscode)
script.on('message', on_message)
script.load()
sys.stdin.read()
