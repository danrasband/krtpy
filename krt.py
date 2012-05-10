import re

def hangulize(text, toEncoding):
  """
    Take romanized Korean text and return
    the hangulized version.
  """
  output = ''
  toLoop = []
  for i in text:
    toLoop.append(i)
  toLoop.reverse()
  # print toLoop
  
  # Set up the vars for the state machine
  state = 'START' # possible states: START, INITIAL, VOWEL, FINAL
  syllable = {}
  hangul = ''
  
  # Start the state machine
  while (len(toLoop) > 0):
    
    # get the next char
    char = toLoop.pop()
    if state == 'START':
      syllable = {}
      # check to make sure it's a letter, if not, just add it to the string
      if char in letters:
        if char in consonantLetters:
          syllable['initial'] = char
          state = 'INITIAL'
          if len(toLoop) == 0:
            if char in nonpachim:
              hangul += hangulize_syllable(syllable)
            else:
              hangul += syllable['initial']
        elif char in vowelLetters:
          syllable['vowel'] = char
          state = 'VOWEL'
          if len(toLoop) == 0:
            if char in moum:
              hangul += hangulize_syllable(syllable)
            else:
              hangul += char
      else:
        if char == '.' and len(toLoop) > 0 and toLoop[-1] in letters:
          if syllable != {}:
            hangul += hangulize_syllable(syllable)
            syllable = {}
            char = ''
          else:
            if char != '.':
              hangul += char
              char = ''
          state = 'START'
        elif char == '<':
          if syllable != {}:
            hangul += hangulize_syllable(syllable)
            syllable = {}
          state = 'SINGLE'
        else:
          # print char + ' not in letters, not a period, and not a lesser than sign'
          if syllable != {}:
            hangul += hangulize_syllable(syllable)
            syllable = {}
          hangul += char
          char = ''
          state = 'START'
    elif state == 'INITIAL':
      if char in letters:
        if char in vowelLetters:
          # todo: but what if this char is 'w' and the next one is a consonant?
          syllable['vowel'] = char
          state = 'VOWEL'
          if char in moum:
            fullVowel = True
        else:
          if syllable['initial'] + char in nonpachim or syllable['initial'] + char in consonantLetters:
            syllable['initial'] = syllable['initial'] + char
          else:
            hangul += hangulize_syllable(syllable)
            syllable = {}
            state = 'START'
      else:
        if char == '.' and len(toLoop) > 0 and toLoop[-1] in letters:
          if syllable != {}:
            hangul += hangulize_syllable(syllable)
            syllable = {}
            char = ''
          else:
            if char != '.':
              hangul += char
              char = ''
          state = 'START'
        elif char == '<':
          if syllable != {}:
            hangul += hangulize_syllable(syllable)
            syllable = {}
          state = 'SINGLE'
        else:
          if syllable != {}:
            hangul += hangulize_syllable(syllable)
            syllable = {}
          hangul += char
          char = ''
          state = 'START'
    elif state == 'VOWEL':
      #print 'state is VOWEL'
      if char in letters:
        if char in vowelLetters:
          if syllable['vowel'] + char in moum:
            syllable['vowel'] = syllable['vowel'] + char
          else:
            hangul += hangulize_syllable(syllable)
            syllable = {}
            syllable['initial'] = ''
            syllable['vowel'] = char
            state = 'VOWEL'
        else:
          syllable['final'] = char
          state = 'FINAL'
      else:
        if char == '.' and len(toLoop) > 0 and toLoop[-1] in letters:
          if syllable != {}:
            hangul += hangulize_syllable(syllable)
            syllable = {}
            char = ''
          else:
            if char != '.':
              hangul += char
              char = ''
          state = 'START'
        elif char == '<':
          if syllable != {}:
            hangul += hangulize_syllable(syllable)
            syllable = {}
          state = 'SINGLE'
        else:
          if syllable != {}:
            hangul += hangulize_syllable(syllable)
            syllable = {}
          hangul += char
          char = ''
          state = 'START'
    elif state == 'FINAL':
      if char in letters:
        if syllable['final'] + char in pachim:
          syllable['final'] = syllable['final'] + char
        else:
          hangul += hangulize_syllable(syllable)
          syllable = {}
          if char in vowelLetters:
            syllable['initial'] = ''
            syllable['vowel'] = char
            state = 'VOWEL'
            if char in moum:
              fullVowel = True
          else:
            syllable['initial'] = char
            state = 'INITIAL'
      else:
        hangul += hangulize_syllable(syllable)
        syllable = {}
        if char == '.' and len(toLoop) > 0 and toLoop[-1] in letters:
          if syllable != {}:
            hangul += hangulize_syllable(syllable)
            syllable = {}
            char = ''
          else:
            if char != '.':
              hangul += char
              char = ''
          state = 'START'
        elif char == '<':
          if syllable != {}:
            hangul += hangulize_syllable(syllable)
            syllable = {}
          state = 'SINGLE'
        else:
          if syllable != {}:
            hangul += hangulize_syllable(syllable)
            syllable = {}
          hangul += char
          char = ''
          state = 'START'
    elif state == 'SINGLE':
      # print 'in state == SINGLE: ',
      # print str(syllable),
      # print "CURRENT LETTER: " + char
      if char in singleLetters:
        # print 'char in singleLetters'
        if 'single' in syllable and char + syllable['single'] in singleLetters:
          # print syllable['single'] + ' in singleLetters'
          syllable['single'] += char
        elif 'single' in syllable and not syllable['single'] + char in singleLetters:
          # print syllable['single'] + char + ' is not in singleLetters'
          hangul += '<' + syllable['single']
          syllable = {}
          if char in vowelLetters:
            syllable['initial'] = ''
            syllable['vowel'] = char
            state = 'VOWEL'
          elif char in consonantLetters:
            syllable['initial'] = char
            state = 'INITIAL'
          else:
            state = 'START'
        else:
          if 'single' in syllable:
            syllable['single'] += char
          else:
            syllable['single'] = char
      elif char == '>':
        # print 'ending single',
        hangul += hangulize_syllable(syllable)
        syllable = {}
        char = ''
        state = 'START'
      else:
        # print char + ' not in singleLetters'
        hangul += char
        syllable = {}
        state = 'START'
    if len(toLoop) == 0:
      if syllable == {}:
        hangul += char
      else:
        if 'single' in syllable:
          hangul += '<' + syllable['single']
        else:
          hangul += hangulize_syllable(syllable)
    continue
  return hangul.encode(toEncoding)

def hangulize_syllable(syl):
  """
    Take romanized Korean word and return a list of its syllables.
  """
  single = vowel = final = None
  initial = ''
  # print str(syl)
  if 'single' in syl:
    single = syl['single']
  if 'initial' in syl:
    initial = syl['initial']
  if 'vowel' in syl:
    vowel = syl['vowel']
  if 'final' in syl:
    final = syl['final']
  #print initial
  #print vowel
  #print final
  if single == None:
    if vowel == None and final == None:
      #print "is single initial"
      single = initial
    elif initial == None and final == None:
      #print 'is single vowel'
      single = vowel
    else:
      #print 'is not single'
      single = None
  
  sIndex = iIndex = vIndex = fIndex = 0
  if single != None:
    if single in singlesDict:
      sIndex = singlesDict[single]
    else:
      return single
    #print 'getting singles index.... ' + str(sIndex)
  else:
    if initial in nonpachimDict:
      iIndex = nonpachimDict[initial]
    else:
      return initial + vowel + final
    if vowel in moumDict:
      vIndex = moumDict[vowel]
    else:
      return initial + vowel + final
    if final in pachimDict:
      fIndex = pachimDict[final]
    else:
      fIndex = None
    sIndex = None
    #print iIndex
    #print vIndex
    #print fIndex
  
  if sIndex != None:
    return unichr(sIndex + 12593)
  else:
    total = 44032
    if iIndex != None:
      total += iIndex * 588
    if vIndex != None:
      total += 28 * vIndex
    if fIndex != None:
      total += fIndex
    return unichr(total)
  return
    
      
    
def romanize(raw, fromEnc = 'utf8', toEnc = 'utf8'):
  """
    Takes a raw string of Korean, a 'from encoding' and a 'to encoding'.
    Returns a romanized string of the text, encoded as specified (default
    'from encoding' is None and default 'to encoding' is utf-8).
  """
  if fromEnc != None:
    raw = raw.decode(fromEnc)
  newString = ''
  for i in range(len(raw)):
    index = gti(raw[i])
    
    # If the index is a single (non-syllabic) hangul letter
    if index in range(12593, 12687):
      index = index - 12593
      if singles[index] and len(newString) > 1 and newString[-1] != ' ':
        newString += '.'
      newString += '<' + singles[index] + '>'
   
    # If the index represents a hangul syllable
    elif index in range(44032, 55204):
      index = index - 44032
      initial = index / 588
      vowel = (index % 588) / 28
      final = (index % 588) % 28
      if len(newString) > 0:
        if nonpachim[initial] == 'g' and newString[-1] == 'n':
          newString += '.'
        elif nonpachim[initial] == '' and newString[-2:len(newString)] == 'ng':
          newString += '.'
        elif (newString[-1] in moum or newString[-2:len(newString)] in moum) and nonpachim[initial] in pachim + nonpachim:
          newString += '.'
        elif nonpachim[initial] == '' and newString[-1] in pachim + nonpachim: 
          newString += '.'
        elif nonpachim[initial] == 'h' and newString[-1] in ['t','k','p','c','n','l']: 
          newString += '.'
        elif newString[-1] + nonpachim[initial] in pachim + nonpachim or (len(nonpachim[initial]) > 1 and newString[-1] + nonpachim[initial][0] in pachim + nonpachim):
          newString += '.' 
      newString += nonpachim[initial]
      newString += moum[vowel]
      newString += pachim[final]
    
    # Otherwise
    else:
      newString += unichr(index).upper()
  return newString.encode(toEnc)


def gti(char):
  """
    Only accepts unicode characters
    Return index of characters
  """
  return ord(char)


# Character lists
singles = ['k', 'kk', 'ks', 'n', 'nc', 'nh', 't', 'tt', 'l', 'lk', 'lm', 'lp', 'ls', 'lth', 'lph', 'lh', 'm', 'p', 'pp', 'ps', 's', 'ss', 'ng', 'c', 'cc', 'ch', 'kh', 'th', 'ph', 'h', 'a', 'ay', 'ya', 'yay', 'e', 'ey', 'ye', 'yey', 'o', 'wa', 'way', 'oy', 'yo', 'wu', 'we', 'wey', 'wi', 'yu', 'u', 'uy', 'i', 'NONE', 'NN', 'NT', 'NS', 'NZ', 'LKS', 'LT', 'LPS', 'LZ', 'LH', 'MP', 'MS', 'MZ', 'MNG', 'PK', 'PT', 'PSK', 'PST', 'PC', 'PTH', 'PNG', 'PPNG', 'SK', 'SL', 'ST', 'SP', 'SC', 'Z', 'NGNG', 'NG', 'NGS', 'NGZ', 'PHNG', 'HH', 'H', 'YOYA', 'YOYAY', 'YOI', 'YUE', 'YUEY', 'YUI', 'A', 'E']
moum = ['a', 'ay', 'ya', 'yay', 'e', 'ey', 'ye', 'yey', 'o', 'wa', 'way', 'oy', 'yo', 'wu', 'we', 'wey', 'wi', 'yu', 'u', 'uy', 'i']
pachim = ['', 'k', 'kk', 'ks', 'n', 'nc', 'nh', 't', 'l', 'lk', 'lm', 'lp', 'ls', 'lth', 'lph', 'lh', 'm', 'p', 'ps', 's', 'ss', 'ng', 'c', 'ch', 'kh', 'th', 'ph', 'h']
nonpachim = ['k', 'kk', 'n', 't', 'tt', 'l', 'm', 'p', 'pp', 's', 'ss', '', 'c', 'cc', 'ch', 'kh', 'th', 'ph', 'h']
letters = ['k', 'n', 't', 'l', 'm', 'p', 's', 'c', 'k', 'h', 'g', 'a', 'y', 'e', 'o', 'w', 'u', 'i']
vowelLetters = ['a', 'e', 'i', 'o', 'u', 'w', 'y']
consonantLetters = ['c', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 's', 't', 'lt', 'lp']
singleLetters = ['k', 'kk', 'ks', 'ns', 'n', 'nc', 'nh', 't', 'tt', 'l', 'lk', 'lm', 'lp', 'ls', 'lth', 'lt', 'lph', 'lt', 'lh', 'm', 'p', 'pp', 'ps', 's', 'ss', 'ng', 'c', 'cc', 'ch', 'kh', 'th', 'ph', 'h', 'a', 'ay', 'ya', 'yay', 'e', 'ey', 'ye', 'yey', 'o', 'wa', 'way', 'oy', 'yo', 'wu', 'we', 'wey', 'wi', 'yu', 'u', 'uy', 'i', 'NONE', 'N', 'NO', 'NON', 'NN', 'NT', 'NS', 'NZ', 'LKS', 'LK', 'L', 'LT', 'LPS', 'LP', 'LZ', 'LH', 'MP', 'M', 'MS', 'MZ', 'MNG', 'MN', 'PK', 'P', 'PT', 'PSK', 'PS', 'PST', 'PC', 'PTH', 'PNG', 'PPNG', 'PP', 'PPN', 'SK', 'S', 'SL', 'ST', 'SP', 'SC', 'Z', 'NGNG', 'NGN', 'NG', 'NGS', 'NGZ', 'PHNG', 'PH', 'PHN', 'HH', 'H', 'YOYA', 'Y', 'YO', 'O', 'YOY', 'YOYAY', 'YOI', 'YUE', 'YU', 'YUEY', 'YUI', 'A', 'E']


# Character dictionaries
singlesDict = {'yey': 37, 'YUE': 89, 'YOYAY': 87, 'tt': 7, 'lm': 10, 'lk': 9, 'lh': 15, 'ls': 12, 'lp': 11, 'wey': 45, 'YUEY': 90, 'yo': 42, 'ya': 32, 'H': 85, 'LPS': 58, 'yu': 47, 'YUI': 91, 'h': 29, 'l': 8, 'p': 17, 't': 6, 'HH': 84, 'ey': 35, 'NGS': 81, 'n': 3, 'LKS': 56, 'NGZ': 82, 'NONE': 51, 'PT': 66, 'PTH': 70, 'PC': 69, 'PK': 65, 'MNG': 64, 'we': 44, 'wa': 39, 'PPNG': 72, 'wi': 46, 'wu': 43, 'PSK': 67, 'c': 23, 'k': 0, 'o': 38, 'PHNG': 83, 's': 20, 'MP': 61, 'MS': 62, 'YOYA': 86, 'lth': 13, 'PST': 68, 'MZ': 63, 'ch': 25, 'cc': 24, 'ps': 19, 'pp': 18, 'yay': 33, 'NN': 52, 'NG': 80, 'NZ': 55, 'way': 40, 'ph': 28, 'NS': 54, 'NT': 53, 'th': 27, 'Z': 78, 'uy': 49, 'SP': 76, 'ST': 75, 'SK': 73, 'ss': 21, 'SL': 74, 'SC': 77, 'ay': 31, 'NGNG': 79, 'nh': 5, 'nc': 4, 'LH': 60, 'ng': 22, 'LT': 57, 'ks': 2, 'LZ': 59, 'A': 92, 'E': 93, 'oy': 41, 'YOI': 88, 'ye': 36, 'kk': 1, 'a': 30, 'e': 34, 'i': 50, 'kh': 26, 'm': 16, 'u': 48, 'lph': 14, 'PNG': 71}
moumDict = {'a': 0, 'we': 14, 'uy': 19, 'yay': 3, 'oy': 11, 'wa': 9, 'ya': 2, 'yo': 12, 'ye': 6, 'o': 8, 'yey': 7, 'i': 20, 'wu': 13, 'ey': 5, 'wi': 16, 'way': 10, 'ay': 1, 'e': 4, 'wey': 15, 'yu': 17, 'u': 18}
pachimDict = {'': 0, 'nc': 5, 'ch': 23, 'nh': 6, 'ps': 18, 'p': 17, 'lm': 10, 'lk': 9, 'lh': 15, 'ng': 21, 'ls': 12, 'lp': 11, 'ph': 26, 'th': 25, 'c': 22, 'ss': 20, 'h': 27, 'k': 1, 'kh': 24, 'm': 16, 'l': 8, 'n': 4, 'ks': 3, 'kk': 2, 's': 19, 't': 7, 'lph': 14, 'lth': 13}
nonpachimDict = {'': 11, 'pp': 8, 'ch': 14, 'ss': 10, 'kk': 1, 'c': 12, 'k': 0, 'kh': 15, 'm': 6, 'l': 5, 'n': 2, 'p': 7, 's': 9, 't': 3, 'th': 16, 'h': 18, 'ph': 17, 'tt': 4, 'cc': 13}
