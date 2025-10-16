'''import random

# Define the days, subjects, and subjects that require a lab session
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
subjects = ['Math', 'Science', 'English', 'History', 'Geography', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Physical Education', 'Art', 'Music']
lab_subjects = ['Physics', 'Chemistry', 'Biology', 'Computer Science']

# Function to generate a timetable
def generate_timetable(days, subjects, lab_subjects):
    timetable = {day: [] for day in days}

    # Assign lab sessions first
    for lab_subject in lab_subjects:
        day = random.choice(days)
        time_slot = f"{random.randint(1, 3)}:00 PM"  # You can customize this based on your schedule
        timetable[day].append(f"{lab_subject} Lab ({time_slot}-{time_slot.replace('PM', 'PM' if 'PM' in time_slot else 'AM')})")

    # Assign remaining subjects
    for day in days:
        remaining_subjects = [subject for subject in subjects if subject not in timetable[day]]
        random.shuffle(remaining_subjects)
        for subject in remaining_subjects:
            timetable[day].append(subject)

    return timetable

# Function to display the timetable
def display_timetable(timetable):
    for day, subjects in timetable.items():
        print(f"{day}: {', '.join(subjects)}")

# Generate and display the timetable
timetable = generate_timetable(days, subjects, lab_subjects)
display_timetable(timetable)

session['vno'] = ''
findPlate = PlateFinder()

# Initialize the Neural Network
model = NeuralNetwork()

cap = cv2.VideoCapture(0)
while (True):
    ret, img = cap.read()
    if ret == True:
        cv2.imshow('original video', img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        # cv2.waitKey(0)
        possible_plates = findPlate.find_possible_plates(img)
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

        if possible_plates is not None:
            for i, p in enumerate(possible_plates):
                chars_on_plate = findPlate.char_on_plate[i]
                recognized_plate, _ = model.label_image_list(chars_on_plate, imageSizeOuput=128)
                print(recognized_plate)

                cv2.imshow('plate', p)
                predicted_result = pytesseract.image_to_string(p, lang='eng',
                                                               config='--oem 3 --psm 6 -c tessedit_char_whitelist = ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                print(predicted_result)

                vno = re.sub(r"[^a-zA-Z0-9]", "", predicted_result)
                print(vno)

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                conn = mysql.connector.connect(user='root', password='', host='localhost',
                                               database='2vehicleQrcodedb')
                cursor = conn.cursor()
                cursor.execute(
                    "select * from  complainttb where VehicleNo='" + str(vno) + "' and Status ='waiting' ")
                data = cursor.fetchone()
                if data:
                    mobbb = data[2]
                    VehicleType = data[7]
                    sendmsg(mobbb, 'Vehicle Found! VehicleType:' + VehicleType)
                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='2vehicleQrcodedb')
                    cursor = conn.cursor()
                    cursor.execute("update  complainttb set Status='Find'   where VehicleNo='" + str(vno) + "' ")
                    conn.commit()
                    conn.close()
                    cap.release()
                    cv2.destroyAllWindows()
                    return "Vehicle Found VehicleType:" + VehicleType

                conn = mysql.connector.connect(user='root', password='', host='localhost',
                                               database='2vehicleQrcodedb')
                cursor = conn.cursor()
                cursor.execute(
                    "select * from insuratb where VehicleNo='" + str(vno) + "' and  ExpiryDate < '" + date + "' ")
                data = cursor.fetchone()
                if data is None:
                    print("VehilceNo Not Found")

                else:
                    mob = data[2]
                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='1numberhelmetdb')
                    cursor = conn.cursor()
                    cursor.execute(
                        "select * from entrytb where Date='" + str(date) + "' and VehicleNo='" + str(vno) + "'")
                    data = cursor.fetchone()
                    if data is None:
                        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                       database='2vehicleQrcodedb')
                        cursor = conn.cursor()
                        cursor.execute(
                            "insert into entrytb values('','" + str(vno) + "','" + str(
                                date) + "','" + str(
                                timeStamp) + "','500','NotPaid')")
                        conn.commit()
                        conn.close()
                        print("Fine Amount Info Saved")

                        sendmsg(mob, " Fine Amount For Insurance Date expiry  RS.500")

                        vnoo = vno
                        cap.release()
                        cv2.destroyAllWindows()

                        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                       database='2vehicleQrcodedb')
                        # cursor = conn.cursor()
                        cur = conn.cursor()
                        cur.execute("SELECT * FROM entrytb ")
                        data = cur.fetchall()

                        return render_template('AdminReport.html', data=data)


                    else:
                        cap.release()
                        cv2.destroyAllWindows()
                        return "Already Fine Amount Info Saved"

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break


    else:
        break
cap.release()
cv2.destroyAllWindows()
return render_template('AdminHome.html')
'''