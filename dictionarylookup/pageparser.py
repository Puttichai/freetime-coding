from lxml import html

def ParsePageContent(content):
    """Extract the content of the page.
    
    """
    tree = html.fromstring(content)
    # Each element contains data for each possible part of speech of this word.
    elements = tree.xpath('//section[@class="gramb"]')
    if len(elements) == 0:
        return None
    
    meanings = [_ParsePerPartOfSpeech(element) for element in elements]
    return meanings

def _ParsePerPartOfSpeech(element):
    """Extract content for each part-of-speech section.
    
    """
    result = dict()
    
    partOfSpeech = element.xpath('.//span[@class="pos"]/text()')[0]
    result['partOfSpeech'] = partOfSpeech

    result['meanings'] = dict()
    definitionElements = element.xpath('.//ul[@class="semb"]/li')
    for defElement in definitionElements:
        index = 1
        # If there is only one meaning for that part of speech, "iteration" will be empty
        iterationElement = defElement.xpath('.//span[@class="iteration"]/text()')
        if len(iterationElement) > 0:
            indexStr = iterationElement[0]
            index = int(indexStr)
            
        meaning = defElement.xpath('.//span[@class="ind"]/text()')[0]
        currentMeaning = dict()
        currentMeaning['main'] = meaning
        # TODO: include other information such as inflections, subsenses, examples
        
        result['meanings'][index] = currentMeaning

    return result
