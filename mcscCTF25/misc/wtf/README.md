## 😄😃😄😃😄

- **Difficulty**: Easy
- **Category**: Miscellaneous
- **Skills Required**: File Metadata Analysis, EXIF Data Extraction

### Description

Is he nodding to the beat or the beat nodding to him 😄😃😄😃😄

This peculiar file with an unusual extension might seem like nothing special at first glance, but hidden within its metadata lies a secret message. The rhythmic emoji in the title might just be hinting at something more than meets the eye.

## Files Provided

- [`😄.wtf`](./😄.wtf) - The mysterious file with emoji filename

## Hints

Sometimes what you're looking for isn't in the content itself, but in the details surrounding it.

## Solution

<details>
<summary>Click to reveal solution</summary>

### Analysis Approach

1. The challenge involves investigating a file with an unusual extension and emoji filename
2. The file's content isn't as important as its metadata
3. Using EXIF data extraction tools reveals hidden information in the file's metadata
4. The flag is stored in the file's Comment field

### Metadata Extraction

```bash
# Use exiftool to extract metadata from the file

┌──(psychosherlock㉿fsociety)-[~/…/labs/mcscCTF25/misc/wtf]
└─$ exiftool 😄.wtf
ExifTool Version Number         : 13.10
File Name                       : 😄.wtf
Directory                       : .
File Size                       : 8.5 MB
File Modification Date/Time     : 2025:08:23 02:40:53+05:30
File Access Date/Time           : 2025:08:25 11:2
....
.....
Comment                         : mcsc{n0d_of_the_ring}
.....
....
```

### Flag

`mcsc{n0d_of_the_ring}`

</details>

## Author

Created by [psychoSherlock](https://github.com/psychoSherlock)
