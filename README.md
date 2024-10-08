## 📘 About the project
HashCracker is a brute force tool for decoding encoded hashes. Using this Python script, you can generate word combinations from predefined character sets and attempt to decode various types of hashes, including MD5, SHA1, SHA224, SHA256, SHA384, SHA512, BLAKE2B, and BLAKE2S.

## 🔧 System Construction
The system was built in Python, with a design focused on the efficient use of multiple threads in parallel. A single thread is responsible for feeding a word list, which is simultaneously processed by the other threads as they become available. Each thread generates hashes for each word in the list and compares them with the stored hashes, continuing until all possible matches are found. The solutions found are recorded in a file throughout the process, optimizing progress tracking.

## 📋 System Requirements

To run HashCracker, you need to have the following software installed:

- 🐍 Python 3.8+
- 📚 Git

The user also needs to be familiar with the terminal.

## 🚀 How to Use

1. First, clone the repository:
```bash
git clone https://github.com/WhitePoodleMoth/HashCracker.git
```

2. Navigate to the project folder:
```bash
cd HashCracker
```

3. You can edit the `main.py` file or create your own:

```python
import HC.BFH
hash_list = ["fcd6eb393e783a20e3db79db0ef57c49","b845f8a24f6821855a4cba4c5a422416"]
_hc = HC.BFH.HashCracker(hash_list,"MD5",10,500,3)
_hc.Crack()
_hc.Checker()
```

4. Now you can run the script:
```bash
python main.py
```

5. The output will be saved in the `HashCracked.txt` file, containing all decoded hashes.

## 👥 Developers
- [WhitePoodleMoth](https://github.com/WhitePoodleMoth)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
