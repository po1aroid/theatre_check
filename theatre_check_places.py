import requests
from lxml import etree

url_search = 'https://www.mariinsky.ru/en/playbill/playbill/'


def main():
    try:
        s = requests.Session()

        res = s.get(url_search)
        tree = etree.HTML(res.text)

        links = tree.xpath("//div[@class='t_button']/a[@class != 'no']/@href")

        for link in links:
            try:
                l_res = s.get('https:%s' % link)
                l_tree = etree.XML(
                    l_res.text[l_res.text.index('<content>') + len('<content>'):l_res.text.index('</content>')])

                time = l_tree.xpath("//time/text()")[0]
                date = l_tree.xpath("//date/text()")[0]
                name = l_tree.xpath("//name/text()")[0]
                hall = l_tree.xpath("//hall/text()")[0]

                print("Performance: %s\nDate: %s %s\nHall: %s\n" % (name, date, time, hall))

                print("Available seats: ")
                try:
                    tickets = l_tree.xpath("//ticket")
                    for t in tickets:
                        print(" ".join(
                            [x.text if x.text else '' for x in
                             t.xpath("*[self::tregion or self::tside or self::trow or self::tplace]")]
                        ))
                except Exception as ex:
                    print(ex)
            except Exception as ex:
                print(ex)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
