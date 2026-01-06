# ESDA Bot – Encoder Testing

## Overview
This guide explains how to test the encoder and motor system using an **STM32 board** and an **Arduino Mega** simultaneously.  
The STM32 reads encoder data and calculates RPM, while the Arduino controls motor speed and direction via an ESC.

---

## Hardware Required
- Arduino Mega board  
- STM32 board  
- Encoder sensor (A3144)  
- Jumper wires  

---

## Software Required
- `encoder_final.zip` (STM32CubeIDE project)  
- `ESC_programming_code.ino` (Arduino IDE sketch)  

---

## Software Setup

---

## STM32CubeIDE Setup

1. Download `encoder_final.zip`.
2. Open **STM32CubeIDE** and create a workspace.
3. Go to: File → Import → Archive File and select `encoder_final.zip`.
4. The project should now appear in the **Project Explorer**.
5. Right-click the project → **Build Project**.
- If errors occur, try **Clean Project** and rebuild.
6. Click **OK** if prompted for code generation.
7. Navigate to: Core → Src → main.c
  This file continuously reads encoder data and calculates RPM.

---

## Running the STM32 Code

1. Ensure the STM32 board is connected via USB.
2. Open the **Command Shell Console** in STM32CubeIDE.

![Command Shell](https://github.com/user-attachments/assets/1e34ea73-27c0-4609-a8c3-e21011bdab83)

3. Identify the COM port:
- **Device Manager → Ports**
<img width="1953" height="1421" alt="image" src="https://github.com/user-attachments/assets/fbd1e3bd-1bb4-4deb-a256-08bfe5f54a16" />

- Locate the ST-Link COM port (e.g. COM3).
4. Configure the console:
- Select the correct COM port
- Leave encoding as default

![COM Port Setup](https://github.com/user-attachments/assets/42226bb0-07cc-4665-8795-f98728913914)

5. Click the **Run (green Play icon)**.
6. Open the console to view RPM printed every 1 second.

---

## Arduino IDE Setup

1. Open `ESC_programming_code.ino`.
2. Connect the **Arduino Mega** via USB.
3. In **Tools → Port**, select the correct COM port.
4. Click **Verify (✔)** and wait for compilation.
5. Click **Upload** and wait for ESC beeping.
6. Open **Tools → Serial Monitor**.

---

## Motor Control Commands

Enter values between **1000–2000**:

| Value | Function |
|------|----------|
| 1500 | Brake |
| >1500 | Forward |
| <1500 | Reverse |

### Notes
- Operate at low speed only:
- Forward: ~1570
- Reverse: ~1450
- Always enter **1500** before reversing direction.

---

## Troubleshooting

### Issue: No Encoder Reading
- Check encoder wiring and connections.
- Verify pin mapping using `encoder_2.ioc`.
- Ensure encoder digital output is connected to **STM32 pin A0**.
- Confirm encoder is powered via **5V**.

![Encoder Pins](https://github.com/user-attachments/assets/a4a2b155-39a9-42b2-85e6-7ace6b7c9e71)
![Encoder Wiring](https://github.com/user-attachments/assets/f56402f4-df38-4c8d-a228-5438c397adee)

---

### Issue: Motor Not Working
- Ensure 24V power cable is connected to ESC.
- Power supply settings:
- Voltage: **24.00V**
- Current limit: **3.00A**
- Ensure **Arduino Pin 9** is connected to ESC **RX** wire.
- Verify motor wires are correctly connected.

![ESC Power](https://github.com/user-attachments/assets/735899c6-1bf6-4378-b20f-b504d1950af9)
![ESC Signal](https://github.com/user-attachments/assets/a38f8fc2-9ad7-407d-b7ab-4e33de0f77ee)



