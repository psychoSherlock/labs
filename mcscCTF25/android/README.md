## Project Azadi

- **Difficulty**: Medium
- **Category**: Android Security
- **Skills Required**: APK Decompilation, Android App Analysis, Base32 Decoding

This application was recovered from the debris of a forgotten hideout destroyed during the final days of British resistance in India.

Among the ashes was a single, scorched device — its storage barely intact. Inside it, this lone application survived, believed to hold the final encrypted oath sworn by Azad's underground network.

No passwords were found.  
No manual.  
No instructions.

They say only the truly worthy — those who understand the spirit of Azad — can unlock its secret.

Will you?

## Files Provided

- [`azadi.apk`](./builds/azadi.apk) - The recovered Android application

## Hints

This APP isn't going to open itself. Peel it apart like a digital onion, and look for the Main. Remember, Freedom doesn't require a key.

## Solution

<details>
<summary>Click to reveal solution</summary>

### Analysis Approach

1. The app is a standard Android application that can be analyzed through decompilation
2. Using tools like JADX-GUI or APKTool, extract and examine the application code
3. Investigate the MainActivity.java file for hidden information
4. Locate an encoded string that serves as the password for the lock screen
5. The encoded string is a base32 representation of the flag

### Decompilation and Flag Extraction

```bash
# Decompile the APK using JADX-GUI or APKTool
# After examining MainActivity.java, find the encoded string
# Decode it using base32

┌──(psychosherlock㉿fsociety)-[~]
└─$ echo "NVRXGY33IF5DIZBRL5HDG5RTOJPUIMJTMRPUMMDSL5EW4ZBRGR6Q" | base32 -d
mcsc{Az4d1_N3v3r_D13d_F0r_Ind14}
```

### Flag

`mcsc{Az4d1_N3v3r_D13d_F0r_Ind14}`

</details>

## Author

Created by [psychoSherlock](https://github.com/psychoSherlock)
