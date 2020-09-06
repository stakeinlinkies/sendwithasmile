
import cv2
from web3 import Web3

ganache_url = "HTTP://127.0.0.1:7545"  #or use infura for mainnet transactions
#infura_url =

web3 = Web3(Web3.HTTPProvider(ganache_url))


account_1 = "0x7d568D709d2435e3af337b1a7e3a01dF3Ea04DAe"  #send from  input('Input the ethereum address from where you want to send ')
account_2 = "0x43216c2f180B550A6592C0E83cC44D25FAf74283"  #send to input('Send to this  ethereum address ')
private_key = "e6b07ba5b1c3405f456a45a3524dfb6b19e036f791766fff52f43eb5a432b7f3"  #private key from account1 (sender)

balance = web3.eth.getBalance(account_1)
print(balance)





nonce = web3.eth.getTransactionCount(account_1)

tx = {
'nonce': nonce,
'to': account_2,
'value': web3.toWei(1, 'ether'),
'gas': 21000,
'gasPrice': web3.toWei('500', 'gwei')
}

print(nonce)




#Face classifier
face_detector = cv2.CascadeClassifier('frontalface.xml')
smile_detector = cv2.CascadeClassifier('smile.xml')

#Grab WebCam feed
webcam = cv2.VideoCapture(1)


#Show the current frame
while True :
    #Read the current frame from webcam video stream
    successful_frame_read, frame = webcam.read()

    #If there's an error, abort
    if not successful_frame_read:
        break
    #Change to grayscale
    frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Detect faces first
    faces = face_detector.detectMultiScale(frame_grayscale)
    #Detect smiles
    smiles = smile_detector.detectMultiScale(frame_grayscale, scaleFactor= 1.7, minNeighbors= 20)
    #Run smile detection within each of those faces
    for (x, y, w, h) in faces :
        #Drow a rectangle around the face
        cv2.rectangle(frame,(x, y), (x+w, y+h), (100, 200, 50), 4)
        #Get the sub frame ( using numpy N-dimensional array slicing )
        the_face = frame[y:y+h, x:x+w]
        #the_face = (x, y, w, h)
        #Change to grayscale
        face_grayscale = cv2.cvtColor(the_face, cv2.COLOR_BGR2GRAY)
        smiles = smile_detector.detectMultiScale(face_grayscale, scaleFactor= 1.7, minNeighbors= 20)

        #Find the smile in the face
        for (x_, y_, w_, h_) in smiles :
            #Drow a rectangle around the face
            cv2.rectangle(the_face,(x_, y_), (x_+w_, y_+h_), (50, 50, 200), 4)
        #Label this face as smiling
        if len(smiles) > 0 :
            cv2.putText(frame, 'you are smiling', (x, y+h+40), fontScale=3, fontFace=cv2.FONT_HERSHEY_PLAIN, color=(255, 255, 255))
            signed_tx = web3.eth.account.signTransaction(tx, private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(web3.toHex(tx_hash))
            balance = web3.eth.getBalance(account_1)
            print(balance)

        else:
            cv2.putText(frame, 'Smile to send tx', (x, y+h+40), fontScale=3, fontFace=cv2.FONT_HERSHEY_PLAIN, color=(255, 255, 255))


    cv2.imshow ('Smile Detector', frame)

    #Display
    cv2.waitKey(1)

#CleanUp
webcam.release()
cv2.destroyAllWindows()



print("success Code Completed  & transaction sent")
