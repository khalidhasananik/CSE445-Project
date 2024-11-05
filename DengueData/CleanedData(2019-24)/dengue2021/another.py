import pandas as pd
from datetime import datetime, timedelta

# Utility class to handle string manipulation
class Util:
    @staticmethod
    def mb_strlen(text):
        return len(text)

    @staticmethod
    def mbCharAt(text, index):
        return text[index]

    @staticmethod
    def subString(text, start, end):
        return text[start:end]

    @staticmethod
    def doCharMap(text, char_map):
        for key, value in char_map.items():
            text = text.replace(key, value)
        return text

util = Util()

# Full Unicode class with all the conversion logic and mappings
class Unicode:
    preConversionMap = {
        ' +':' ',
        'yy':'y',
        'vv':'v',
        '­­':'­',
        'y&':'y',
        '„&':'„',
        '‡u':'u‡',
        'wu':'uw',
        ' ,':',',
        ' \\|':'\\|',
        '\\\\ ':'',
        ' \\\\':'',
        '\\\\':'',
        '\n +':'\n',
        ' +\n':'\n',
        '\n\n\n\n\n':'\n\n',
        '\n\n\n\n':'\n\n',
        '\n\n\n':'\n\n'
    }

    # conversionMap = {
    #     'Av': 'আ', 'A': 'অ', 'B': 'ই', 'C': 'ঈ', 'D': 'উ', 'E': 'ঊ', 'F': 'ঋ', 'G': 'এ', 'H': 'ঐ', 'I': 'ও', 'J': 'ঔ',
    #     'K': 'ক', 'L': 'খ', 'M': 'গ', 'N': 'ঘ', 'O': 'ঙ', 'P': 'চ', 'Q': 'ছ', 'R': 'জ', 'S': 'ঝ', 'T': 'ঞ',
    #     'U': 'ট', 'V': 'ঠ', 'W': 'ড', 'X': 'ঢ', 'Y': 'ণ', 'Z': 'ত', '_': 'থ', '`': 'দ', 'a': 'ধ', 'b': 'ন',
    #     'c': 'প', 'd': 'ফ', 'e': 'ব', 'f': 'ভ', 'g': 'ম', 'h': 'য', 'i': 'র', 'j': 'ল', 'k': 'শ', 'l': 'ষ', 'm': 'স', 'n': 'হ',
    #     'o': 'ড়', 'p': 'ঢ়', 'q': 'য়', 'r': 'ৎ', 's': 'ং', 't': 'ঃ', 'u': 'ঁ',
    #     '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯',
    #     'v': 'া', 'w': 'ি', 'x': 'ী', 'y': 'ু', 'z': 'ু', '“': 'ু', '–': 'ু', '~': 'ূ', 'ƒ': 'ূ', '‚': 'ূ', '„': 'ৃ',
    #     '†': 'ে', '‡': 'ে', 'ˆ': 'ৈ', '‰': 'ৈ', 'Š': 'ৗ', '\\|': '।', '\\&': '্‌'
    # }

    conversionMap = {
    # Vowels
    'Av': 'আ', 'A': 'অ', 'B': 'ই', 'C': 'ঈ', 'D': 'উ', 'E': 'ঊ', 'F': 'ঋ',
    'G': 'এ', 'H': 'ঐ', 'I': 'ও', 'J': 'ঔ',

    # Consonants
    'K': 'ক', 'L': 'খ', 'M': 'গ', 'N': 'ঘ', 'O': 'ঙ', 'P': 'চ', 'Q': 'ছ',
    'R': 'জ', 'S': 'ঝ', 'T': 'ঞ', 'U': 'ট', 'V': 'ঠ', 'W': 'ড', 'X': 'ঢ',
    'Y': 'ণ', 'Z': 'ত', '_': 'থ', '`': 'দ', 'a': 'ধ', 'b': 'ন', 'c': 'প',
    'd': 'ফ', 'e': 'ব', 'f': 'ভ', 'g': 'ম', 'h': 'য', 'i': 'র', 'j': 'ল',
    'k': 'শ', 'l': 'ষ', 'm': 'স', 'n': 'হ', 'o': 'ড়', 'p': 'ঢ়', 'q': 'য়',
    'r': 'ৎ', 's': 'ং', 't': 'ঃ', 'u': 'ঁ',

    # Numbers
    '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫',
    '6': '৬', '7': '৭', '8': '৮', '9': '৯',

    # Kars and other signs
    'v': 'া', 'w': 'ি', 'x': 'ী', 'y': 'ু', 'z': 'ূ', '~': 'ূ', '„': 'ৃ',
    '†': 'ে', '‡': 'ে', 'ˆ': 'ৈ', '‰': 'ৈ', 'Š': 'ৗ', '\\|': '।', '\\&': '্‌',

    # Merged from main_char
    '|': '।', 'Ô': '‘', 'Õ': '’', 'Ò': '“', 'Ó': '”', 'ª¨': '্র্য',
    '¤cÖ': 'ম্প্র', 'i¨': 'র‌্য', '²': 'ক্ষ্ম', '°': 'ক্ক', '±': 'ক্ট',
    '³': 'ক্ত', 'K¡': 'ক্ব', '¯Œ': 'স্ক্র', 'µ': 'ক্র', 'K¬': 'ক্ল',
    '¶': 'ক্ষ', '·': 'ক্স', '¸': 'গু', '»': 'গ্ধ', 'Mœ': 'গ্ন', 'M¥': 'গ্ম',
    'M­': 'গ্ল', 'Mªy': 'গ্রু', '¼': 'ঙ্ক', '•¶': 'ঙ্ক্ষ', '•L': 'ঙ্খ',
    '½': 'ঙ্গ', '•N': 'ঙ্ঘ', '”Q¡': 'চ্ছ্ব', '”P': 'চ্চ', '”Q': 'চ্ছ',
    '”T': 'চ্ঞ', '¾¡': 'জ্জ্ব', '¾': 'জ্জ', 'À': 'জ্ঝ', 'Á': 'জ্ঞ',
    'R¡': 'জ্ব', 'Â': 'ঞ্চ', 'Ã': 'ঞ্ছ', 'Ä': 'ঞ্জ', 'Å': 'ঞ্ঝ', 'Æ': 'ট্ট',
    'U¡': 'ট্ব', 'U¥': 'ট্ম', 'Ç': 'ড্ড', 'È': 'ণ্ট', 'É': 'ণ্ঠ', 'Ý': 'ন্স',
    'Ê': 'ণ্ড', 'š‘': 'ন্তু', 'Y^': 'ণ্ব', 'Ë¡': 'ত্ত্ব', 'Ë': 'ত্ত',
    'Ì': 'ত্থ', 'Zœ': 'ত্ন', 'Z¥': 'ত্ম', 'š—¡': 'ন্ত্ব', 'Z¡': 'ত্ব',
    '_¡': 'থ্ব', '˜M': 'দ্গ', '˜N': 'দ্ঘ', 'Ï': 'দ্দ', '×': 'দ্ধ',
    '˜¡': 'দ্ব', 'Ø': 'দ্ব', '™¢': 'দ্ভ', 'Ù': 'দ্ম', '`ª“': 'দ্রু',
    'aŸ': 'ধ্ব', 'a¥': 'ধ্ম', '›U': 'ন্ট', 'Ú': 'ন্ঠ', 'Û': 'ন্ড',
    'š¿': 'ন্ত্র', 'š—': 'ন্ত', '¯¿': 'স্ত্র', 'Î': 'ত্র', 'š’': 'ন্থ',
    '›`': 'ন্দ', '›Ø': 'ন্দ্ব', 'Ü': 'ন্ধ', 'bœ': 'ন্ন', 'š^': 'ন্ব',
    'b¥': 'ন্ম', 'Þ': 'প্ট', 'ß': 'প্ত', 'cœ': 'প্ন', 'à': 'প্প',
    'cø': 'প্ল', 'á': 'প্স', 'd¬': 'ফ্ল', 'â': 'ব্জ', 'ã': 'ব্দ',
    'ä': 'ব্ধ', 'eŸ': 'ব্ব', 'e­': 'ব্ল', 'å': 'ভ্র', 'gœ': 'ম্ন',
    '¤ú': 'ম্প', 'ç': 'ম্ফ', '¤^': 'ম্ব', '¤¢': 'ম্ভ', '¤£': 'ম্ভ্র',
    '¤§': 'ম্ম', '¤­': 'ম্ল', 'ª': '্র', 'i“': 'রু', 'iƒ': 'রূ',
    'é': 'ল্ক', 'ê': 'ল্গ', 'ë': 'ল্ট', 'ì': 'ল্ড', 'í': 'ল্প',
    'î': 'ল্ফ', 'j¦': 'ল্ব', 'j¥': 'ল্ম', 'jø': 'ল্ল', 'ï': 'শু',
    'ð': 'শ্চ', 'kœ': 'শ্ন', 'k¦': 'শ্ব', 'k¥': 'শ্ম', 'k­': 'শ্ল',
    '®‹': 'ষ্ক', '®Œ': 'ষ্ক্র', 'ó': 'ষ্ট', 'ô': 'ষ্ঠ', 'ò': 'ষ্ণ',
    '®ú': 'ষ্প', 'õ': 'ষ্ফ', '®§': 'ষ্ম', '¯‹': 'স্ক', '÷': 'স্ট',
    'ö': 'স্খ', '¯Í': 'স্ত', '¯‘': 'স্তু', '¯’': 'স্থ', 'mœ': 'স্ন',
    '¯ú': 'স্প', 'ù': 'স্ফ', '¯^': 'স্ব', '¯§': 'স্ম', '¯­': 'স্ল',
    'û': 'হু', 'nè': 'হ্ণ', 'nŸ': 'হ্ব', 'ý': 'হ্ন', 'þ': 'হ্ম',
    'n¬': 'হ্ল', 'ü': 'হৃ', '©': 'র্', '«': '্র', '¨': '্য', '&': '্'
}


    proConversionMap = {'্্': '্'}

    # postConversionMap = {
    #     '০ঃ': '০:', '১ঃ': '১:', '২ঃ': '২:', '৩ঃ': '৩:', '৪ঃ': '৪:', '৫ঃ': '৫:', '৬ঃ': '৬:', '৭ঃ': '৭:', '৮ঃ': '৮:', '৯ঃ': '৯:',
    #     ' ঃ': ':', '\nঃ': '\n:', ']ঃ': ']:', '\\[ঃ': '\\[:', '  ': ' ', 'অা': 'আ', '্‌্‌': '্‌'
    # }

    postConversionMap = {
    # Specific fixes for character alignment
    'Ö': '্র',  # চট্টগÖাম -> চট্টগ্রাম
    'ø': '্ল',  # কূমিলøা -> কুমিল্লা
    'ÿ': 'ক্ষ',  # লÿীপুর -> লক্ষ্মীপুর, সাতÿীরা -> সাতক্ষীরা

    # Fix for Chandrabindu misplacement
    'ঁা': 'াঁ',  # Fix for চঁাদপুর -> চাঁদপুর

    # Duplicate character and spacing fixes
    'অা': 'আ',  # Fix for accidental duplication of vowel signs
    '।।': '।',  # Fix for double punctuation (full stop)
    '  ': ' ',   # Remove double spaces
    ' ।': '।',   # Fix space before punctuation
    ': ': ':',   # Remove extra space after colon

    # Handling conjuncts and special characters
    '০ঃ': '০:', '১ঃ': '১:', '২ঃ': '২:', '৩ঃ': '৩:', '৪ঃ': '৪:',
    '৫ঃ': '৫:', '৬ঃ': '৬:', '৭ঃ': '৭:', '৮ঃ': '৮:', '৯ঃ': '৯:',
    ' ঃ': ':', '\nঃ': '\n:', ']ঃ': ']:', '\\[ঃ': '\\[:',

    # General character replacements
    '্‌্‌': '্‌',  # Handle repeated Hoshonto
    '্র': '্র',    # Prevent double replacement of '্র'

    # Fix for vowel combinations and placement issues
    'ো': 'ো',  # Fix split of 'ো' vowel
    'ৌ': 'ৌ',  # Fix split of 'ৌ' vowel

    # Removing unwanted artifacts from conversion
    'Ô': '‘', 'Õ': '’', 'Ò': '“', 'Ó': '”',

    # Handling specific space issues
    ' ': ' ',   # Ensure single spaces only
    '। ': '।',  # Fix space after punctuation
    ' : ': ':',  # Correct colons with spaces
    ' | ': '।',  # Incorrect space around pipe character
}





    def convertBijoyToUnicode(self, srcString):
        if not srcString:
            return srcString

        srcString = util.doCharMap(srcString, self.preConversionMap)
        srcString = util.doCharMap(srcString, self.conversionMap)
        srcString = self.reArrangeUnicodeConvertedText(srcString)
        srcString = util.doCharMap(srcString, self.postConversionMap)
        return srcString

    def reArrangeUnicodeConvertedText(self, text):
        i = 0
        while i < util.mb_strlen(text):
            # Reordering vowel + HALANT + consonant
            if (i > 0 and util.mbCharAt(text, i) == '্' and (self.IsBanglaKar(util.mbCharAt(text, i - 1)) or self.IsBanglaNukta(util.mbCharAt(text, i - 1))) and i < util.mb_strlen(text) - 1):
                temp = util.subString(text, 0, i - 1)
                temp += util.mbCharAt(text, i)
                temp += util.mbCharAt(text, i + 1)
                temp += util.mbCharAt(text, i - 1)
                temp += util.subString(text, i + 2, util.mb_strlen(text))
                text = temp

            # Handling RA + HALANT + vowel to rearrange as Vowel + RA + HALANT
            if (i > 0 and i < util.mb_strlen(text) - 1 and util.mbCharAt(text, i) == '্' and util.mbCharAt(text, i - 1) == 'র' and self.IsBanglaKar(util.mbCharAt(text, i + 1))):
                temp = util.subString(text, 0, i - 1)
                temp += util.mbCharAt(text, i + 1)
                temp += util.mbCharAt(text, i - 1)
                temp += util.mbCharAt(text, i)
                temp += util.subString(text, i + 2, util.mb_strlen(text))
                text = temp

            # Pre-kar should be placed before the consonant (for i-kar, e-kar, etc.)
            if (i < util.mb_strlen(text) - 1 and self.IsBanglaPreKar(util.mbCharAt(text, i)) and not self.IsSpace(util.mbCharAt(text, i + 1))):
                temp = util.subString(text, 0, i)
                j = 1
                while ((i + j) < util.mb_strlen(text) - 1 and self.IsBanglaBanjonborno(util.mbCharAt(text, i + j))):
                    if ((i + j) < util.mb_strlen(text) and self.IsBanglaHalant(util.mbCharAt(text, i + j + 1))):
                        j += 2
                    else:
                        break

                temp += util.subString(text, i + 1, i + j + 1)

                # Handle double vowels like e-kar + a-kar forming o-kar
                l = 0
                if (util.mbCharAt(text, i) == 'ে' and util.mbCharAt(text, i + j + 1) == 'া'):
                    temp += "ো"
                    l = 1
                elif (util.mbCharAt(text, i) == 'ে' and util.mbCharAt(text, i + j + 1) == "ৗ"):
                    temp += "ৌ"
                    l = 1
                else:
                    temp += util.mbCharAt(text, i)

                temp += util.subString(text, i + j + l + 1, util.mb_strlen(text))
                text = temp
                i += j

            i += 1
        return text

    # Helper functions for Bangla characters
    def IsBanglaPreKar(self, c):
        return c in ('ি', 'ৈ', 'ে')

    def IsBanglaPostKar(self, c):
        return c in ('া', 'ো', 'ৌ', 'ৗ', 'ু', 'ূ', 'ী', 'ৃ')

    def IsBanglaKar(self, c):
        return self.IsBanglaPreKar(c) or self.IsBanglaPostKar(c)

    def IsBanglaNukta(self, c):
        return c == 'ঁ'

    def IsBanglaHalant(self, c):
        return c == '্'

    def IsBanglaBanjonborno(self, c):
        return c in 'কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁ'

    def IsSpace(self, c):
        return c in (' ', '\t', '\n', '\r')

# Function to convert Bijoy text to Unicode
def convert_bijoy_text(text, unicode_converter):
    if isinstance(text, str) and len(text.strip()) > 0:
        try:
            # Convert Bijoy-encoded text to Unicode
            return unicode_converter.convertBijoyToUnicode(text)
        except Exception as e:
            print(f"Error converting text: {e}")
            return text  # Return the original text if there's an error
    return text  # If it's not a string or empty, return the original text

# Function to apply Bijoy to Unicode conversion to each cell in a DataFrame
# def apply_conversion(df, unicode_converter):
#     return df.applymap(lambda cell: convert_bijoy_text(cell, unicode_converter))


# Function to apply Bijoy to Unicode conversion to each cell in a DataFrame
def apply_conversion(df, unicode_converter):
    # Use DataFrame.apply() with lambda for element-wise operation
    return df.apply(lambda col: col.map(lambda cell: convert_bijoy_text(cell, unicode_converter)))


# Function to keep only the 5th (E) and 9th (I) columns using positional indexing
# def select_columns(df):
#     return df.iloc[:, [4, 8]]  # Select the 5th (index 4) and 9th (index 8) columns

# # select all columns
# def select_columns(df):
#     # Remove the first 3 rows and select the 5th (index 4) and 10th (index 9) columns
#     # return df.iloc[3:, [4, 9]]
#     # return df
#     return df.iloc[1:, [4, 8]]


def select_columns(df):
    # Select columns using iloc
    result = df.iloc[5:, [4, 8]]

    # Fill the first value with ঢাকা
    result.iloc[0, 0] = 'ঢাকা'

    return result


# Generate date sequence from 31-12-19 to 01-01-19 in reverse order
# def generate_dates(start_date, num_days):
#     start = datetime.strptime(start_date, "%d-%m-%y")
#     dates = [(start - timedelta(days=x)).strftime("%d-%m-%y") for x in range(num_days)]
#     return dates

def generate_dates(start_date, num_days):
    start = datetime.strptime(start_date, "%d-%m-%y")
    dates = [(start - timedelta(days=x)) for x in range(num_days)]
    return dates

# Load the Excel file
input_file = 'dengue21.xlsx'  # Replace with your actual Excel file path
excel_file = pd.ExcelFile(input_file)

# Initialize the Unicode converter
unicode_converter = Unicode()

# Generate sheet names using dates (assuming number of sheets corresponds to number of days)
sheet_dates = generate_dates("31-12-21", len(excel_file.sheet_names))
# sheet_dates = generate_dates("31-12-21", 1)

# Iterate over each sheet, convert the text, select 'E' and 'I' columns, and save the result
# for idx, sheet_name in enumerate(excel_file.sheet_names):
#     # Read the current sheet into a DataFrame
#     df = pd.read_excel(input_file, sheet_name=sheet_name)

#     # Apply Bijoy to Unicode conversion to the DataFrame
#     df_converted = apply_conversion(df, unicode_converter)

#     # Select only the 'E' and 'I' columns (5th and 9th columns)
#     df_selected = select_columns(df_converted)

#     # Define the output filename based on the generated dates
#     # output_file = f"{sheet_dates[idx]}.xlsx"

#     output_file = f"{sheet_dates[idx].strftime('%Y-%m-%d')}.xlsx"

#     # Save the selected columns and converted data to a new Excel file
#     df_selected.to_excel(output_file, index=False)

#     print(f"Converted and saved {output_file}")

for idx, sheet_name in enumerate(excel_file.sheet_names):
    # Read the current sheet into a DataFrame
    df = pd.read_excel(input_file, sheet_name=sheet_name)

    # Apply Bijoy to Unicode conversion to the DataFrame
    df_converted = apply_conversion(df, unicode_converter)

    # Select only the 'E' and 'I' columns (5th and 9th columns)
    df_selected = select_columns(df_converted)

    # Define the output filename based on the generated dates in 'YYYY-MM-DD' format
    output_file = f"{sheet_dates[idx].strftime('%Y-%m-%d')}.xlsx"

    # Save the selected columns and converted data to a new Excel file
    df_selected.to_excel(output_file, index=False)

    print(f"Converted and saved {output_file}")



# version 6
# import pandas as pd
# from datetime import datetime, timedelta

# # Utility class to handle string manipulation
# class Util:
#     @staticmethod
#     def mb_strlen(text):
#         return len(text)

#     @staticmethod
#     def mbCharAt(text, index):
#         return text[index]

#     @staticmethod
#     def subString(text, start, end):
#         return text[start:end]

#     @staticmethod
#     def doCharMap(text, char_map):
#         for key, value in char_map.items():
#             text = text.replace(key, value)
#         return text

# util = Util()

# # Full Unicode class with all the conversion logic and mappings
# class Unicode:
#     preConversionMap = {
#         ' +':' ',
#         'yy':'y',
#         'vv':'v',
#         '­­':'­',
#         'y&':'y',
#         '„&':'„',
#         '‡u':'u‡',
#         'wu':'uw',
#         ' ,':',',
#         ' \\|':'\\|',
#         '\\\\ ':'',
#         ' \\\\':'',
#         '\\\\':'',
#         '\n +':'\n',
#         ' +\n':'\n',
#         '\n\n\n\n\n':'\n\n',
#         '\n\n\n\n':'\n\n',
#         '\n\n\n':'\n\n'
#     }

#     conversionMap = {
#         'Av': 'আ', 'A': 'অ', 'B': 'ই', 'C': 'ঈ', 'D': 'উ', 'E': 'ঊ', 'F': 'ঋ', 'G': 'এ', 'H': 'ঐ', 'I': 'ও', 'J': 'ঔ',
#         'K': 'ক', 'L': 'খ', 'M': 'গ', 'N': 'ঘ', 'O': 'ঙ', 'P': 'চ', 'Q': 'ছ', 'R': 'জ', 'S': 'ঝ', 'T': 'ঞ',
#         'U': 'ট', 'V': 'ঠ', 'W': 'ড', 'X': 'ঢ', 'Y': 'ণ', 'Z': 'ত', '_': 'থ', '`': 'দ', 'a': 'ধ', 'b': 'ন',
#         'c': 'প', 'd': 'ফ', 'e': 'ব', 'f': 'ভ', 'g': 'ম', 'h': 'য', 'i': 'র', 'j': 'ল', 'k': 'শ', 'l': 'ষ', 'm': 'স', 'n': 'হ',
#         'o': 'ড়', 'p': 'ঢ়', 'q': 'য়', 'r': 'ৎ', 's': 'ং', 't': 'ঃ', 'u': 'ঁ',
#         '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯',
#         'v': 'া', 'w': 'ি', 'x': 'ী', 'y': 'ু', 'z': 'ু', '“': 'ু', '–': 'ু', '~': 'ূ', 'ƒ': 'ূ', '‚': 'ূ', '„': 'ৃ',
#         '†': 'ে', '‡': 'ে', 'ˆ': 'ৈ', '‰': 'ৈ', 'Š': 'ৗ', '\\|': '।', '\\&': '্‌'
#     }

#     proConversionMap = {'্্': '্'}

#     postConversionMap = {
#         '০ঃ': '০:', '১ঃ': '১:', '২ঃ': '২:', '৩ঃ': '৩:', '৪ঃ': '৪:', '৫ঃ': '৫:', '৬ঃ': '৬:', '৭ঃ': '৭:', '৮ঃ': '৮:', '৯ঃ': '৯:',
#         ' ঃ': ':', '\nঃ': '\n:', ']ঃ': ']:', '\\[ঃ': '\\[:', '  ': ' ', 'অা': 'আ', '্‌্‌': '্‌'
#     }

#     def convertBijoyToUnicode(self, srcString):
#         if not srcString:
#             return srcString

#         srcString = util.doCharMap(srcString, self.preConversionMap)
#         srcString = util.doCharMap(srcString, self.conversionMap)
#         srcString = self.reArrangeUnicodeConvertedText(srcString)
#         srcString = util.doCharMap(srcString, self.postConversionMap)
#         return srcString

#     def reArrangeUnicodeConvertedText(self, text):
#         i = 0
#         while i < util.mb_strlen(text):
#             # Reordering vowel + HALANT + consonant
#             if (i > 0 and util.mbCharAt(text, i) == '্' and (self.IsBanglaKar(util.mbCharAt(text, i - 1)) or self.IsBanglaNukta(util.mbCharAt(text, i - 1))) and i < util.mb_strlen(text) - 1):
#                 temp = util.subString(text, 0, i - 1)
#                 temp += util.mbCharAt(text, i)
#                 temp += util.mbCharAt(text, i + 1)
#                 temp += util.mbCharAt(text, i - 1)
#                 temp += util.subString(text, i + 2, util.mb_strlen(text))
#                 text = temp

#             # Handling RA + HALANT + vowel to rearrange as Vowel + RA + HALANT
#             if (i > 0 and i < util.mb_strlen(text) - 1 and util.mbCharAt(text, i) == '্' and util.mbCharAt(text, i - 1) == 'র' and self.IsBanglaKar(util.mbCharAt(text, i + 1))):
#                 temp = util.subString(text, 0, i - 1)
#                 temp += util.mbCharAt(text, i + 1)
#                 temp += util.mbCharAt(text, i - 1)
#                 temp += util.mbCharAt(text, i)
#                 temp += util.subString(text, i + 2, util.mb_strlen(text))
#                 text = temp

#             # Pre-kar should be placed before the consonant (for i-kar, e-kar, etc.)
#             if (i < util.mb_strlen(text) - 1 and self.IsBanglaPreKar(util.mbCharAt(text, i)) and not self.IsSpace(util.mbCharAt(text, i + 1))):
#                 temp = util.subString(text, 0, i)
#                 j = 1
#                 while ((i + j) < util.mb_strlen(text) - 1 and self.IsBanglaBanjonborno(util.mbCharAt(text, i + j))):
#                     if ((i + j) < util.mb_strlen(text) and self.IsBanglaHalant(util.mbCharAt(text, i + j + 1))):
#                         j += 2
#                     else:
#                         break

#                 temp += util.subString(text, i + 1, i + j + 1)

#                 # Handle double vowels like e-kar + a-kar forming o-kar
#                 l = 0
#                 if (util.mbCharAt(text, i) == 'ে' and util.mbCharAt(text, i + j + 1) == 'া'):
#                     temp += "ো"
#                     l = 1
#                 elif (util.mbCharAt(text, i) == 'ে' and util.mbCharAt(text, i + j + 1) == "ৗ"):
#                     temp += "ৌ"
#                     l = 1
#                 else:
#                     temp += util.mbCharAt(text, i)

#                 temp += util.subString(text, i + j + l + 1, util.mb_strlen(text))
#                 text = temp
#                 i += j

#             i += 1
#         return text

#     # Helper functions for Bangla characters
#     def IsBanglaPreKar(self, c):
#         return c in ('ি', 'ৈ', 'ে')

#     def IsBanglaPostKar(self, c):
#         return c in ('া', 'ো', 'ৌ', 'ৗ', 'ু', 'ূ', 'ী', 'ৃ')

#     def IsBanglaKar(self, c):
#         return self.IsBanglaPreKar(c) or self.IsBanglaPostKar(c)

#     def IsBanglaNukta(self, c):
#         return c == 'ঁ'

#     def IsBanglaHalant(self, c):
#         return c == '্'

#     def IsBanglaBanjonborno(self, c):
#         return c in 'কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁ'

#     def IsSpace(self, c):
#         return c in (' ', '\t', '\n', '\r')

# # Function to convert Bijoy text to Unicode
# def convert_bijoy_text(text, unicode_converter):
#     if isinstance(text, str) and len(text.strip()) > 0:
#         try:
#             # Convert Bijoy-encoded text to Unicode
#             return unicode_converter.convertBijoyToUnicode(text)
#         except Exception as e:
#             print(f"Error converting text: {e}")
#             return text  # Return the original text if there's an error
#     return text  # If it's not a string or empty, return the original text

# # Function to apply Bijoy to Unicode conversion to each cell in a DataFrame
# def apply_conversion(df, unicode_converter):
#     return df.applymap(lambda cell: convert_bijoy_text(cell, unicode_converter))

# # # Function to keep only 'E' and 'I' columns
# # def select_columns(df):
# #     return df[['E', 'I']]  # Assuming columns are named 'E' and 'I', otherwise use df.iloc[:, [4, 8]] for position-based indexing

# # Function to keep only the 5th (E) and 9th (I) columns using positional indexing
# def select_columns(df):
#     return df.iloc[:, [4, 8]]  # Select the 5th (index 4) and 9th (index 8) columns

# # Generate date sequence from 31-12-19 to 01-01-19 in reverse order
# def generate_dates(start_date, num_days):
#     start = datetime.strptime(start_date, "%d-%m-%y")
#     dates = [(start - timedelta(days=x)).strftime("%d-%m-%y") for x in range(num_days)]
#     return dates

# # Load the Excel file
# input_file = 'dengue19.xlsx'  # Replace with your actual Excel file path
# excel_file = pd.ExcelFile(input_file)

# # Initialize the Unicode converter
# unicode_converter = Unicode()

# # Generate sheet names using dates (assuming number of sheets corresponds to number of days)
# sheet_dates = generate_dates("31-12-19", len(excel_file.sheet_names))

# # Iterate over each sheet, convert the text, select 'E' and 'I' columns, and save the result
# for idx, sheet_name in enumerate(excel_file.sheet_names):
#     # Read the current sheet into a DataFrame
#     df = pd.read_excel(input_file, sheet_name=sheet_name)

#     # Apply Bijoy to Unicode conversion to the DataFrame
#     df_converted = apply_conversion(df, unicode_converter)

#     # Select only the 'E' and 'I' columns (5th and 9th columns)
#     df_selected = select_columns(df_converted)

#     # Define the output filename based on the generated dates
#     output_file = f"{sheet_dates[idx]}.xlsx"

#     # Save the selected columns and converted data to a new Excel file
#     df_selected.to_excel(output_file, index=False)

#     print(f"Converted and saved {output_file}")

# version 5
# import pandas as pd

# # Utility class to handle string manipulation
# class Util:
#     @staticmethod
#     def mb_strlen(text):
#         return len(text)

#     @staticmethod
#     def mbCharAt(text, index):
#         return text[index]

#     @staticmethod
#     def subString(text, start, end):
#         return text[start:end]

#     @staticmethod
#     def doCharMap(text, char_map):
#         for key, value in char_map.items():
#             text = text.replace(key, value)
#         return text

# util = Util()

# # Full Unicode class with all the conversion logic and mappings
# class Unicode:
#     preConversionMap = {
#         ' +':' ',
#         'yy':'y',
#         'vv':'v',
#         '­­':'­',
#         'y&':'y',
#         '„&':'„',
#         '‡u':'u‡',
#         'wu':'uw',
#         ' ,':',',
#         ' \\|':'\\|',
#         '\\\\ ':'',
#         ' \\\\':'',
#         '\\\\':'',
#         '\n +':'\n',
#         ' +\n':'\n',
#         '\n\n\n\n\n':'\n\n',
#         '\n\n\n\n':'\n\n',
#         '\n\n\n':'\n\n'
#     }

#     conversionMap = {
#         'Av': 'আ', 'A': 'অ', 'B': 'ই', 'C': 'ঈ', 'D': 'উ', 'E': 'ঊ', 'F': 'ঋ', 'G': 'এ', 'H': 'ঐ', 'I': 'ও', 'J': 'ঔ',
#         'K': 'ক', 'L': 'খ', 'M': 'গ', 'N': 'ঘ', 'O': 'ঙ', 'P': 'চ', 'Q': 'ছ', 'R': 'জ', 'S': 'ঝ', 'T': 'ঞ',
#         'U': 'ট', 'V': 'ঠ', 'W': 'ড', 'X': 'ঢ', 'Y': 'ণ', 'Z': 'ত', '_': 'থ', '`': 'দ', 'a': 'ধ', 'b': 'ন',
#         'c': 'প', 'd': 'ফ', 'e': 'ব', 'f': 'ভ', 'g': 'ম', 'h': 'য', 'i': 'র', 'j': 'ল', 'k': 'শ', 'l': 'ষ', 'm': 'স', 'n': 'হ',
#         'o': 'ড়', 'p': 'ঢ়', 'q': 'য়', 'r': 'ৎ', 's': 'ং', 't': 'ঃ', 'u': 'ঁ',
#         '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯',
#         'v': 'া', 'w': 'ি', 'x': 'ী', 'y': 'ু', 'z': 'ু', '“': 'ু', '–': 'ু', '~': 'ূ', 'ƒ': 'ূ', '‚': 'ূ', '„': 'ৃ',
#         '†': 'ে', '‡': 'ে', 'ˆ': 'ৈ', '‰': 'ৈ', 'Š': 'ৗ', '\\|': '।', '\\&': '্‌'
#     }

#     proConversionMap = {'্্': '্'}

#     postConversionMap = {
#         '০ঃ': '০:', '১ঃ': '১:', '২ঃ': '২:', '৩ঃ': '৩:', '৪ঃ': '৪:', '৫ঃ': '৫:', '৬ঃ': '৬:', '৭ঃ': '৭:', '৮ঃ': '৮:', '৯ঃ': '৯:',
#         ' ঃ': ':', '\nঃ': '\n:', ']ঃ': ']:', '\\[ঃ': '\\[:', '  ': ' ', 'অা': 'আ', '্‌্‌': '্‌'
#     }

#     def convertBijoyToUnicode(self, srcString):
#         if not srcString:
#             return srcString

#         srcString = util.doCharMap(srcString, self.preConversionMap)
#         srcString = util.doCharMap(srcString, self.conversionMap)
#         srcString = self.reArrangeUnicodeConvertedText(srcString)
#         srcString = util.doCharMap(srcString, self.postConversionMap)
#         return srcString

#     def reArrangeUnicodeConvertedText(self, text):
#         i = 0
#         while i < util.mb_strlen(text):
#             # Reordering vowel + HALANT + consonant
#             if (i > 0 and util.mbCharAt(text, i) == '্' and (self.IsBanglaKar(util.mbCharAt(text, i - 1)) or self.IsBanglaNukta(util.mbCharAt(text, i - 1))) and i < util.mb_strlen(text) - 1):
#                 temp = util.subString(text, 0, i - 1)
#                 temp += util.mbCharAt(text, i)
#                 temp += util.mbCharAt(text, i + 1)
#                 temp += util.mbCharAt(text, i - 1)
#                 temp += util.subString(text, i + 2, util.mb_strlen(text))
#                 text = temp

#             # Handling RA + HALANT + vowel to rearrange as Vowel + RA + HALANT
#             if (i > 0 and i < util.mb_strlen(text) - 1 and util.mbCharAt(text, i) == '্' and util.mbCharAt(text, i - 1) == 'র' and self.IsBanglaKar(util.mbCharAt(text, i + 1))):
#                 temp = util.subString(text, 0, i - 1)
#                 temp += util.mbCharAt(text, i + 1)
#                 temp += util.mbCharAt(text, i - 1)
#                 temp += util.mbCharAt(text, i)
#                 temp += util.subString(text, i + 2, util.mb_strlen(text))
#                 text = temp

#             # Pre-kar should be placed before the consonant (for i-kar, e-kar, etc.)
#             if (i < util.mb_strlen(text) - 1 and self.IsBanglaPreKar(util.mbCharAt(text, i)) and not self.IsSpace(util.mbCharAt(text, i + 1))):
#                 temp = util.subString(text, 0, i)
#                 j = 1
#                 while ((i + j) < util.mb_strlen(text) - 1 and self.IsBanglaBanjonborno(util.mbCharAt(text, i + j))):
#                     if ((i + j) < util.mb_strlen(text) and self.IsBanglaHalant(util.mbCharAt(text, i + j + 1))):
#                         j += 2
#                     else:
#                         break

#                 temp += util.subString(text, i + 1, i + j + 1)

#                 # Handle double vowels like e-kar + a-kar forming o-kar
#                 l = 0
#                 if (util.mbCharAt(text, i) == 'ে' and util.mbCharAt(text, i + j + 1) == 'া'):
#                     temp += "ো"
#                     l = 1
#                 elif (util.mbCharAt(text, i) == 'ে' and util.mbCharAt(text, i + j + 1) == "ৗ"):
#                     temp += "ৌ"
#                     l = 1
#                 else:
#                     temp += util.mbCharAt(text, i)

#                 temp += util.subString(text, i + j + l + 1, util.mb_strlen(text))
#                 text = temp
#                 i += j

#             i += 1
#         return text

#     # Helper functions for Bangla characters
#     def IsBanglaPreKar(self, c):
#         return c in ('ি', 'ৈ', 'ে')

#     def IsBanglaPostKar(self, c):
#         return c in ('া', 'ো', 'ৌ', 'ৗ', 'ু', 'ূ', 'ী', 'ৃ')

#     def IsBanglaKar(self, c):
#         return self.IsBanglaPreKar(c) or self.IsBanglaPostKar(c)

#     def IsBanglaNukta(self, c):
#         return c == 'ঁ'

#     def IsBanglaHalant(self, c):
#         return c == '্'

#     def IsBanglaBanjonborno(self, c):
#         return c in 'কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎংঃঁ'

#     def IsSpace(self, c):
#         return c in (' ', '\t', '\n', '\r')

# # Function to convert Bijoy text to Unicode
# def convert_bijoy_text(text, unicode_converter):
#     if isinstance(text, str) and len(text.strip()) > 0:
#         try:
#             # Convert Bijoy-encoded text to Unicode
#             return unicode_converter.convertBijoyToUnicode(text)
#         except Exception as e:
#             print(f"Error converting text: {e}")
#             return text  # Return the original text if there's an error
#     return text  # If it's not a string or empty, return the original text

# # Function to apply Bijoy to Unicode conversion to each cell in a DataFrame
# def apply_conversion(df, unicode_converter):
#     return df.applymap(lambda cell: convert_bijoy_text(cell, unicode_converter))

# # Load the Excel file
# input_file = 'dengue19.xlsx'  # Replace with your actual Excel file path
# excel_file = pd.ExcelFile(input_file)

# # Initialize the Unicode converter
# unicode_converter = Unicode()

# # Iterate over each sheet, convert the text, and save the result
# for idx, sheet_name in enumerate(excel_file.sheet_names, start=1):
#     # Read the current sheet into a DataFrame
#     df = pd.read_excel(input_file, sheet_name=sheet_name)

#     # Apply Bijoy to Unicode conversion to the DataFrame
#     df_converted = apply_conversion(df, unicode_converter)

#     # Define the output filename
#     output_file = f"sheet{idx}_unicode.xlsx"

#     # Save the converted DataFrame to a new Excel file
#     df_converted.to_excel(output_file, index=False)

#     print(f"Converted and saved {output_file}")


# version 4
# import pandas as pd

# # Utility functions needed for the Unicode class
# class Util:
#     @staticmethod
#     def mb_strlen(text):
#         return len(text)

#     @staticmethod
#     def mbCharAt(text, index):
#         return text[index]

#     @staticmethod
#     def subString(text, start, end):
#         return text[start:end]

#     @staticmethod
#     def doCharMap(text, char_map):
#         for key, value in char_map.items():
#             text = text.replace(key, value)
#         return text

# util = Util()

# # Full Unicode class with all the conversion logic and mappings
# class Unicode:

#     preConversionMap = {
#         ' +':' ',
#         'yy':'y',
#         'vv':'v',
#         '­­':'­',
#         'y&':'y',
#         '„&':'„',
#         '‡u':'u‡',
#         'wu':'uw',
#         ' ,':',',
#         ' \\|':'\\|',
#         '\\\\ ':'',
#         ' \\\\':'',
#         '\\\\':'',
#         '\n +':'\n',
#         ' +\n':'\n',
#         '\n\n\n\n\n':'\n\n',
#         '\n\n\n\n':'\n\n',
#         '\n\n\n':'\n\n'
#     }

#     conversionMap = {
#         'Av': 'আ', 'A': 'অ', 'B': 'ই', 'C': 'ঈ', 'D': 'উ', 'E': 'ঊ', 'F': 'ঋ', 'G': 'এ', 'H': 'ঐ', 'I': 'ও', 'J': 'ঔ',
#         'K': 'ক', 'L': 'খ', 'M': 'গ', 'N': 'ঘ', 'O': 'ঙ', 'P': 'চ', 'Q': 'ছ', 'R': 'জ', 'S': 'ঝ', 'T': 'ঞ',
#         'U': 'ট', 'V': 'ঠ', 'W': 'ড', 'X': 'ঢ', 'Y': 'ণ', 'Z': 'ত', '_': 'থ', '`': 'দ', 'a': 'ধ', 'b': 'ন',
#         'c': 'প', 'd': 'ফ', 'e': 'ব', 'f': 'ভ', 'g': 'ম', 'h': 'য', 'i': 'র', 'j': 'ল', 'k': 'শ', 'l': 'ষ', 'm': 'স', 'n': 'হ',
#         'o': 'ড়', 'p': 'ঢ়', 'q': 'য়', 'r': 'ৎ', 's': 'ং', 't': 'ঃ', 'u': 'ঁ',
#         '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯',
#         'v': 'া', 'w': 'ি', 'x': 'ী', 'y': 'ু', 'z': 'ু', '“': 'ু', '–': 'ু', '~': 'ূ', 'ƒ': 'ূ', '‚': 'ূ', '„': 'ৃ',
#         '†': 'ে', '‡': 'ে', 'ˆ': 'ৈ', '‰': 'ৈ', 'Š': 'ৗ', '\\|': '।', '\\&': '্‌'
#         # Add the rest of the characters from your conversionMap here...
#     }

#     proConversionMap = {'্্': '্'}

#     postConversionMap = {
#         '০ঃ': '০:', '১ঃ': '১:', '২ঃ': '২:', '৩ঃ': '৩:', '৪ঃ': '৪:', '৫ঃ': '৫:', '৬ঃ': '৬:', '৭ঃ': '৭:', '৮ঃ': '৮:', '৯ঃ': '৯:',
#         ' ঃ': ':', '\nঃ': '\n:', ']ঃ': ']:', '\\[ঃ': '\\[:', '  ': ' ', 'অা': 'আ', '্‌্‌': '্‌'
#     }

#     def convertBijoyToUnicode(self, srcString):
#         if not srcString:
#             return srcString

#         srcString = util.doCharMap(srcString, self.preConversionMap)
#         srcString = util.doCharMap(srcString, self.conversionMap)
#         srcString = self.reArrangeUnicodeConvertedText(srcString)
#         srcString = util.doCharMap(srcString, self.postConversionMap)
#         return srcString

#     def reArrangeUnicodeConvertedText(self, text):
#         # Rearranging the converted text for proper Unicode structure (simplified)
#         return text

# # Function to convert Bijoy text to Unicode
# def convert_bijoy_text(text, unicode_converter):
#     if isinstance(text, str) and len(text.strip()) > 0:
#         try:
#             return unicode_converter.convertBijoyToUnicode(text)
#         except Exception as e:
#             print(f"Error converting text: {e}")
#             return text
#     return text

# # Function to apply Bijoy to Unicode conversion to each cell in a DataFrame
# def apply_conversion(df, unicode_converter):
#     return df.applymap(lambda cell: convert_bijoy_text(cell, unicode_converter))

# # Load the Excel file
# input_file = 'dengue21.xlsx' # Replace with your actual Excel file path
# excel_file = pd.ExcelFile(input_file)

# # Initialize the Unicode converter
# unicode_converter = Unicode()

# # Iterate over each sheet, convert the text, and save the result
# for idx, sheet_name in enumerate(excel_file.sheet_names, start=1):
#     # Read the current sheet into a DataFrame
#     df = pd.read_excel(input_file, sheet_name=sheet_name)

#     # Apply Bijoy to Unicode conversion to the DataFrame
#     df_converted = apply_conversion(df, unicode_converter)

#     # Define the output filename
#     output_file = f"sheet{idx}_unicode.xlsx"

#     # Save the converted DataFrame to a new Excel file
#     df_converted.to_excel(output_file, index=False)

#     print(f"Converted and saved {output_file}")




# version 3
# import pandas as pd
# from converter import convert_bijoy_to_unicode  # Import the function from the package

# # Function to handle Bijoy to Unicode conversion using text files
# def convert_bijoy_text(text):
#     with open("bijoy_temp.txt", "w", encoding="utf-8") as f:
#         f.write(text)

#     # Convert the temporary Bijoy text file to Unicode using the package's function
#     convert_bijoy_to_unicode('bijoy_temp.txt', 'unicode_temp.txt')

#     # Read back the converted text from the Unicode file
#     with open("unicode_temp.txt", "r", encoding="utf-8") as f:
#         unicode_text = f.read()

#     return unicode_text

# # Function to apply the Bijoy to Unicode conversion to DataFrame cells
# def apply_conversion(text):
#     if isinstance(text, str) and len(text.strip()) > 0:
#         try:
#             return convert_bijoy_text(text)
#         except Exception as e:
#             print(f"Error converting text: {e}")
#             return text
#     return text

# # Path to the large Excel file with multiple sheets
# input_file = 'dengue21.xlsx'

# # Load the Excel file
# excel_file = pd.ExcelFile(input_file)

# # Iterate over each sheet, convert the text, and save as separate files
# for idx, sheet_name in enumerate(excel_file.sheet_names, start=1):
#     # Read the current sheet
#     df = pd.read_excel(input_file, sheet_name=sheet_name)

#     # Apply Bijoy to Unicode conversion to all cells
#     df = df.applymap(apply_conversion)

#     # Define the output filename (e.g., sheet1_unicode.xlsx, sheet2_unicode.xlsx, etc.)
#     output_file = f"sheet{idx}_unicode.xlsx"

#     # Save the converted sheet as a new Excel file
#     df.to_excel(output_file, index=False)

#     print(f"Converted and saved {output_file}")

# version 2
# import pandas as pd

# # Define the complete Bijoy to Unicode mapping
# bijoy_to_unicode_map = {
#     "Av": "অ", "Avi": "আ", "w": "ই", "wi": "ঈ", "x": "উ", "xi": "ঊ",
#     "c": "এ", "e": "ঐ", "kv": "ও", "K": "ঔ", "†": "া", "‡": "ি",
#     "ˆ": "ী", "‰": "ু", "Š": "ূ", "‹": "ৃ", "f": "ক", "f¨": "খ",
#     "g": "গ", "g¨": "ঘ", "h": "ঙ", "i": "চ", "i¨": "ছ", "j": "জ",
#     "j¨": "ঝ", "k": "ঞ", "l": "ট", "l¨": "ঠ", "m": "ড", "m¨": "ঢ",
#     "n": "ণ", "o": "ত", "o¨": "থ", "p": "দ", "p¨": "ধ", "q": "ন",
#     "r": "প", "r¨": "ফ", "s": "ব", "s¨": "ভ", "t": "ম", "u": "য",
#     "v": "র", "w": "ল", "x": "শ", "y": "ষ", "z": "স", "a": "হ",
#     "|": "ড়", "}": "ঢ়", "~": "য়", "¡": "ৎ", "¢": "ং", "£": "ঃ",
#     "¤": "ঁ"
# }

# def convert_bijoy_to_unicode(text):
#     """Convert Bijoy-encoded text to Unicode"""
#     if not isinstance(text, str):
#         return text
#     for bijoy_char, unicode_char in bijoy_to_unicode_map.items():
#         text = text.replace(bijoy_char, unicode_char)
#     return text

# # Path to the large Excel file with 365 sheets
# input_file = 'dengue21.xlsx'

# # Load the Excel file
# excel_file = pd.ExcelFile(input_file)

# # Iterate over each sheet, convert the text, and save as separate files
# for idx, sheet_name in enumerate(excel_file.sheet_names, start=1):
#     # Read the current sheet
#     df = pd.read_excel(input_file, sheet_name=sheet_name)

#     # Apply Bijoy to Unicode conversion to all cells
#     df = df.applymap(convert_bijoy_to_unicode)

#     # Define the output filename (e.g., sheet1.xlsx, sheet2.xlsx, etc.)
#     output_file = f"sheet{idx}_unicode.xlsx"

#     # Save the converted sheet as a new Excel file
#     df.to_excel(output_file, index=False)

#     print(f"Converted and saved {output_file}")


# version 1
# import pandas as pd

# # Path to your input Excel file
# input_file = 'dengue21.xlsx'

# # Load the Excel file
# excel_file = pd.ExcelFile(input_file)

# # Iterate over each sheet index and name
# for idx, sheet_name in enumerate(excel_file.sheet_names, start=1):
#     # Read each sheet into a DataFrame
#     df = pd.read_excel(input_file, sheet_name=sheet_name)

#     # Define the output filename as sheet1.xlsx, sheet2.xlsx, etc.
#     output_file = f"sheet{idx}.xlsx"

#     # Save the DataFrame to a new Excel file
#     df.to_excel(output_file, index=False)

#     print(f"Saved sheet {idx} to {output_file}")
