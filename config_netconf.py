from ncclient import manager

m = manager.connect(
    host="192.168.56.102",
    port=830,
    username="admin",
    password="admin",
    hostkey_verify=False
)

config = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>Contetras-Troncoso-Roa</hostname>
    <interface>
      <Loopback>
        <name>11</name>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

m.edit_config(target='running', config=config)
