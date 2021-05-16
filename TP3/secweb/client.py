import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

aes_key = get_random_bytes(16)


SocketClient = socket.socket()
host = socket.gethostname()
port = 18071
SocketClient.connect(("127.0.0.1", port))
Cle_publique=b""

while True:
    recu=SocketClient.recv(1024)
    Cle_publique+=recu
    if b'-----END PUBLIC KEY-----' in Cle_publique:        
        # Start sending AES key =======================
        print("Start sending AES key ...")
        print(f"key   : {aes_key}")
        public_k = RSA.importKey(Cle_publique)
        keyo_rsa_pub = PKCS1_OAEP.new(public_k)

        # send AES key 
        resultat_chiffre = keyo_rsa_pub.encrypt(aes_key)
        SocketClient.send(resultat_chiffre)

        # send a dummy message
        dummy_data = b"IKHLEF Ali"
        cipher = AES.new(aes_key, AES.MODE_ECB)
        print(f"original_data :{dummy_data}")
        ciphered_data = cipher.encrypt(pad(dummy_data, AES.block_size))
        print(f"cipher : {ciphered_data}")
        SocketClient.send(ciphered_data)

        break



print("Lancement serveur ... ")
while True:
    MessageATransmettre=input().encode()
    # Chiffre le message lu du clavier (MessageATransmettre)
    # Utilisez la methode encrypt de objet_cle_rsa_publique
    # Mettez le resultat dans resultat_chiffre
    
    

    cipher = AES.new(aes_key, AES.MODE_ECB)
    resultat_chiffre = cipher.encrypt(
        pad(MessageATransmettre, AES.block_size)
    )
    print(resultat_chiffre)
    SocketClient.send(resultat_chiffre)

    if(MessageATransmettre==b"Fin"):
        break
        print( "Deconnexion de :",addrclient)

SocketClient.close()