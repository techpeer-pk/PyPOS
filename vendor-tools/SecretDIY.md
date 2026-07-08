# PyPOS-Lite Machine-Lock Licensing — Secret DIY Guide
**INTERNAL ONLY — kabhi client ya installer/vendor ko na dein ya na dikhayein.**

Ye document poora explain karta hai ke anti-piracy/machine-lock mechanism kaise kaam karta hai, aur har situation mein aapko step-by-step kya karna hai.

---

## 1. Ye Mechanism Hai Kyun

Problem: `PyPOS-Lite.exe` ek normal file hai — koi bhi (client ka local computer dealer/"vendor" installer) isay copy karke doosre shops ko bhi bech sakta tha, bina aapko kuch diye. Isay rokne ke liye har PC ke liye **alag license key** banayi jaati hai jo **sirf usi PC pe** kaam karti hai.

---

## 2. Core Concept (Simple Zabaan Mein)

Ye ek **lock aur chaabi** wala system hai, jahan:

- **Lock** = app ke andar embedded ek "public key" (`PyPOS-Lite/services/license.py` mein) — sab `.exe` copies mein same hoti hai, ye secret nahi hai
- **Chaabi** = "private key" — sirf aapke paas hai (`C:\Users\TechPeer\PyPOS-Vendor-Keys\private_key.pem`), kabhi kisi `.exe` ke andar nahi jaati
- **Machine ID** = har PC ka apna unique fingerprint (uske hardware se banaya jaata hai — Windows Machine GUID + disk serial + hostname ka hash)
- **License Key** = aapki private key se us specific Machine ID ko "sign" karke banaya gaya signature

App check karta hai: "Ye License Key, is Machine ID ke liye, meri (public) key se match karta hai?" — agar haan, activate ho jata hai. Kisi aur PC pe wahi key kaam nahi karegi kyunke Machine ID alag hoga.

**Important:** Ye ek asymmetric (Ed25519) system hai — matlab app khud sirf verify kar sakta hai, generate nahi. Sirf aap (private key ke malik) naye keys bana sakte hain. Isi liye koi bhi `.exe` ko reverse-engineer kar ke bhi apne liye naya valid key nahi bana sakta.

---

## 3. Kaunsi File Kahan Hai

| File | Kya Hai | Kisko Milegi |
|------|---------|--------------|
| `PyPOS-Lite/services/license.py` | Public key + verification logic | Client ko (ye `.exe` ke andar hi jaati hai) |
| `PyPOS-Lite/ui/activation.py` | Activation screen (Machine ID dikhata hai, key leta hai) | Client ko |
| `vendor-tools/keygen.py` | Naya License Key banane ka tool | **Sirf aapke paas** (kabhi client/installer ko nahi) |
| `C:\Users\TechPeer\PyPOS-Vendor-Keys\private_key.pem` | Asli secret — private key | **Sirf aapke paas, kabhi kisi ko nahi** |
| `PyPOS-Lite/HELP-VENDOR.txt` | Installer ke liye simple guide | Installer/client ko (USB ke sath) |
| `vendor-tools/HELP-ME.txt` | Aapke liye operational checklist | Sirf aap |
| `vendor-tools/SecretDIY.md` (ye file) | Poora mechanism explain karta hai | Sirf aap |

---

## 4. STEP-BY-STEP: Naya Client Onboard Karna (Har Sale Pe Ye Karna Hai)

1. Client/installer `.exe` ko unke PC pe copy karke chalata hai
2. "ACTIVATION REQUIRED" screen aati hai, jisme unka **Machine ID** dikhta hai (jaise `7B93-8325-D104-5DE9`)
3. Wo Machine ID aapko WhatsApp/message karte hain
4. **Aap apne PC pe (jahan private_key.pem hai) ye chalayein:**
   ```
   cd K:\PyPOS\vendor-tools
   python keygen.py <UNKA-MACHINE-ID>
   ```
5. Output mein "License Key" milegi — wahi unhe wapas bhej dein
6. Wo License Key Activation screen mein paste kar ke "Activate" dabate hain → App khul jata hai (Dashboard)

**Note:** Agar aap kisi **doosre laptop** pe (alag Windows username ke sath) `keygen.py` chala rahe hain, hardcoded default path (`C:\Users\TechPeer\...`) us laptop pe nahi milega. Us waqt path batayein:
```
python keygen.py <MACHINE-ID> --key "D:\jahan-bhi-restore-ki\private_key.pem"
```
Ya ek dafa environment variable set kar dein (`PYPOS_VENDOR_KEY`), phir har baar `--key` likhne ki zaroorat nahi.

**Bas itna hi.** Ek baar activate hone ke baad, us PC pe dobara kabhi activation screen nahi aayegi (jab tak wo `data.db` delete na karein).

---

## 5. STEP-BY-STEP: Isi PC Pe Dobara Activation Chahiye Ho (Data Loss/Fresh Folder)

Agar client ka `data.db` corrupt/delete ho jaye, ya app ko naye folder mein install karein (**same PC**):

1. App phir activation maangega, same Machine ID dikhayega (kyunke hardware same hai)
2. Aapko **naya key generate karne ki zaroorat nahi** — jo purani key pehle di thi, wahi **dobara kaam karegi**, bas dobara paste karni hai
3. Purani keys ka record rakhna faydemand hai (e.g. ek simple Excel/notes file: Client Name → Machine ID → License Key), taake aapko dobara `keygen.py` chalane ki zaroorat na pare agar client dobara maange

---

## 6. STEP-BY-STEP: Code Mein Bug Fix / Naya Feature — Naya EXE Banana

**Sabse important cheez samajhne wali:** License **`.exe` ke andar nahi, `data.db` ke andar hoti hai.** Isliye:

1. `.py` files mein fix/change karein
2. Naya build banayein:
   ```
   cd K:\PyPOS\PyPOS-Lite
   python -m PyInstaller --onefile --windowed --name PyPOS-Lite --icon=assets\icon.ico --add-data "assets;assets" main.py
   ```
3. `dist\PyPOS-Lite.exe` client ko bhej dein (WhatsApp/USB/email)
4. Client sirf **purane `.exe` ko naye se replace kare**, `data.db` ko haath na lagayein
5. **Koi naya activation nahi chahiye** — app naye `.exe` mein bhi wahi `data.db` padhega, jisme purani valid key already saved hai

---

## 7. Private Key Lost Ho Jaye Tu Kya Hota Hai

- **Already activated clients:** Koi asar nahi, wo hamesha chalte rahenge (verification sirf public key se hoti hai, jo already `.exe` ke andar embedded hai)
- **Naye clients onboard karna:** **Ruk jayega** — naya key generate nahi kar sakenge
- **Purane client ka PC change ho:** Unke liye naya key nahi bana payenge (jab tak naya keypair na banayein aur naya `.exe` distribute karein — jo sirf future ke liye kaam karega, purane already-shipped exe ka public key retroactively update nahi hota)

**Isi liye backup zaroori tha** (neeche dekhein).

---

## 8. Private Key Backup — Status (Already Done)

Do backups already bana chuke hain:

1. **Digital:** `private_key.pem` manually copy ki gayi — password manager (secure note) + encrypted USB mein
2. **Paper (cold backup):** `PRINT-ME-private_key_backup.html` se ek QR code + SHA-256 checksum print kiya gaya, jo physically safe jagah (locker/drawer) mein rakha hai

**Restore process (agar kabhi zaroorat pare):**
1. Paper pe jo QR code hai, usay kisi bhi phone se scan karein → decode hoga to plain text milega (ye pura PEM file content hai)
2. Us text ko exactly `private_key.pem` naam ki file mein save karein
3. Us file ka SHA-256 checksum nikal kar, paper pe print hui checksum se match karein (confirm karne ke liye ke sahi restore hua)
4. Ab `keygen.py` phir se normal kaam karega

---

## 9. Security Rules — Kabhi Ye Na Karein

- ❌ `private_key.pem` ko kabhi email, WhatsApp, cloud (unencrypted) pe na bhejein
- ❌ `vendor-tools/` folder client/installer ko kabhi na dein (sirf built `.exe` + `HELP-VENDOR.txt` dein)
- ❌ Naya vendor keypair kabhi "just in case" generate na karein — isse **saare purane clients ki activation tootegi** jab unhe naya `.exe` milega. Sirf tab karein jab private key leak/lost ho chuki ho
- ❌ Ek hi License Key do alag machines ko na dein (kaam nahi karegi — key Machine ID se cryptographically tied hai, force karna bhi mumkin nahi)

---

## 10. Quick Reference — Sab Se Common Commands

```
# Naya EXE build karna
cd K:\PyPOS\PyPOS-Lite
python -m PyInstaller --onefile --windowed --name PyPOS-Lite --icon=assets\icon.ico --add-data "assets;assets" main.py

# Naye client ke liye License Key generate karna
cd K:\PyPOS\vendor-tools
python keygen.py <MACHINE-ID>

# Apna khud ka Machine ID nikalna (testing ke liye)
cd K:\PyPOS\PyPOS-Lite
python -c "from services.license import get_machine_id; print(get_machine_id())"
```
