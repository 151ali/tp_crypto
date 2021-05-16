import socket
import _thread as thread
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def Traiter_Connexion(connexion_avec_client,adresse_client):
    global public_k, keyo_rsa_pr,have_aes_key

    MessageRec=b''
    print ("Connexion de la machine = ", adresse_client)
    # Transmettre le contenu de la cle publique apres la connexion
    # Utilisez la methode send de connexion_avec_client pour
    # transmettre contenu_clepublique
    # (A FAIRE 1) ajoutez l'instruction dans cette ligne
    
    connexion_avec_client.send(public_k)

    try:
        while True:
            MessageRec=connexion_avec_client.recv(1024)
            # Dechiffre le message recu (MessageRec)
            # Utilisez la methode decrypt de la cle prive (objet_cle_rsa_prive)
            # Affectez le resulta du dechiffrement a MessageRec
            
            if have_aes_key == True :
                print(f"I have AES key {have_aes_key}") 
                print(f"cipher : {MessageRec}")           
                cipher = AES.new(aes_key, AES.MODE_ECB)
                original_data = unpad(
                    cipher.decrypt(MessageRec), 
                    AES.block_size
                ) 
                print(f"original_data :{original_data}")

            if have_aes_key == False:
                aes_key = keyo_rsa_pr.decrypt(MessageRec)
                print(f"key : \n{aes_key}\n\n")
                have_aes_key = True

            

                

            if MessageRec==b"Fin":
                break
    except  Exception as e:
        print(f"Deconnexion : {e}")
    print("Deconnexion de :",adresse_client)
    try:
        connexion_avec_client.close()
    except:
        pass



SocketServeur = socket.socket()
host = socket.gethostname()
port = 18071
SocketServeur.bind(("127.0.0.1", port))
SocketServeur.listen(5)

have_aes_key = False

public_k = open("keys/public.pem","rb").read()

private_k = RSA.importKey(open("keys/private.pem","rb").read())
keyo_rsa_pr = PKCS1_OAEP.new(private_k)


print("Lancement serveur ...")

while True:
    ConnexionAUnClient, addrclient = SocketServeur.accept()
    thread.start_new_thread(Traiter_Connexion,(ConnexionAUnClient,addrclient))