import unittest
from bs4 import BeautifulSoup
from src.restaurants.sport_cafe import SportCafe


class TestSportCafe(unittest.IsolatedAsyncioTestCase):
    
    async def test_process_data(self):
        sport_cafe = SportCafe("https://www.sport-cafe.cz/#tydenni-menu", "Sport Cafe")
        
        with open("test_data/sport_cafe/sport_cafe.html", "r", encoding="utf-8") as test_days_file:
            test_days = test_days_file.read()
        
        soup = BeautifulSoup(test_days, "html.parser")
        all_h4 = soup.findAll("h4")
        food_h4 = all_h4[1:-2]
        
        sport_cafe._process_data(food_h4)
        
        expected_value = {
            'Pondělí': ['Polévka (k menu zdarma)30 Kč\nČočková se zeleninou',
                        'Menu I160 Kč\nSpaghetti pomodoro- těstoviny s kuřecím masem, kukuřicí, olivami v rajčatové '
                        'omáčce \nsypané parmezánem',
                        'Menu II170 Kč\nPečená krůtí prsa na timiánu, lehký čočkový salát beluga s grilovanou zeleninou',
                        'Menu III185 Kč\nItalský hovězí tataráček podávaný s grilovanou ciabattou, konfitovaným '
                        'česnekem\n\t     a malým caprese salátkem',
                        'Menu IV210 Kč\nTaco de Beef Sport Cafe-tacos v kukuřičné tortille s trhaným hovězím masem, '
                        'naší BBQ cibulkou \n             salsou pico de galo, sypané čedarem, zakysanou smetanou, '
                        'quacamole dresink a čerstvá limetka',
                        'Menu V165 Kč\nSmažený sýr, bramborové hrnanolky, zelný coleslaw salátek',
                        'Menu VI165 Kč\nPizza  Aldo – (rajčatové sugo, sýr, šunka, cibule, uzený sýr)',
                        'Menu VII165 Kč\nFIT Lyonský salát - mix salátových listů s cherry rajčátky a čekankou '
                        'propojený medovo-hořčičným  \n                      dresinkem, parmská šunka, '
                        'zastřené vajíčko, rozpečená bagetka'],
            'Úterý': ['Polévka (k menu zdarma)30 Kč\nKuřecí vývar s nudlemi',
                      'Menu I160 Kč\nKuřecí steak s broskvý zapečený sýrem Eidam, bramborové hranolky, jemný výpek',
                      'Menu II170 Kč\nPečená krůtí prsa na timiánu, lehký čočkový salát beluga s grilovanou zeleninou',
                      'Menu III185 Kč\nItalský hovězí tataráček podávaný s grilovanou ciabattou, konfitovaným '
                      'česnekem\n\t     a malým caprese salátkem',
                      'Menu IV210 Kč\nTaco de Beef Sport Cafe-tacos v kukuřičné tortille s trhaným hovězím masem, '
                      'naší BBQ cibulkou \n             salsou pico de galo, sypané čedarem, zakysanou smetanou, '
                      'quacamole dresink a čerstvá limetka',
                      'Menu V165 Kč\nSmažený sýr, bramborové hrnanolky, zelný coleslaw salátek',
                      'Menu VI165 Kč\nø32 cm Pizza  Aldo – (rajčatové sugo, sýr, šunka, cibule, uzený sýr)',
                      'Menu VII165 Kč\nFIT Lyonský salát - mix salátových listů s cherry rajčátky a čekankou '
                      'propojený medovo-hořčičným  \n                      dresinkem, parmská šunka, '
                      'zastřené vajíčko, rozpečená bagetka'],
            'Středa': ['Polévka (k menu zdarma)30 Kč\nPórková s bramborem',
                       'Menu I160 Kč\nSmažený drůbeží karbanátek s mačkaným bramborem na cibulce, čalamáda',
                       'Menu II170 Kč\nKuřecí steak zapečený rajčaty a mozzarellou, lehká tomatová omáčka, bramborové '
                       'hranolky \n              zdobené lístky rukoly',
                       'Menu III185 Kč\nVepřový steak z kotlety, gorgonzolová omáčka s vlašskými ořechy, '
                       'domácí americké brambory',
                       'Menu IV210 Kč\nSport Cafe ciabatta burger - filírovaný kuřecí steak v rozpečené ciabatte, '
                       'slaninová majonéza \n             nakládaná zelenina, cibulová marmeláda, batátové hranolky, '
                       'tatarská omáčka',
                       'Menu V165 Kč\nSmažený sýr, bramborové hranolky, zelný coleslaw salátek',
                       'Menu VI165 Kč\nPizza  Siciliana– (rajčatový základ, sýr, česnek, klobáska, artyčoky, rajčata)',
                       'Menu VII165 Kč\nFIT Sport poke bowl- losos gravlax, rýže, edamame (sojové fazole), ředkev, '
                       'červené zelí, nakládaný  \n                       zázvor, okurek, ananas, avokádová dresink, '
                       'zdobené sezamem a jalapeňo papričkou',
                       'Menu VIII165 Kč\nSmažený kuřecí řízek servírovaný s bramborovou kaší a zelným coleslaw salátkem'],
            'Čtvrtek': ['Polévka (k menu zdarma)30 Kč\nHovězí vývar s celestýnskými nudlemi',
                        'Menu I160 Kč\nVepřové kostky na houbách se šťouchaným bramborem',
                        'Menu II170 Kč\nKuřecí steak zapečený rajčaty a mozzarellou, lehká tomatová omáčka, '
                        'bramborové hranolky \n              zdobené lístky rukoly',
                        'Menu III185 Kč\nVepřový steak z kotlety, gorgonzolová omáčka s vlašskými ořechy, '
                        'domácí americké brambory',
                        'Menu IV210 Kč\n\nSport Cafe ciabatta burger - filírovaný kuřecí steak v rozpečené ciabatte, '
                        'slaninová majonéza \n             nakládaná zelenina, cibulová marmeláda, batátové hranolky, '
                        'tatarská omáčka',
                        'Menu V165 Kč\nSmažený sýr, bramborové hranolky, zelný coleslaw salátek',
                        'Menu VI165 Kč\nPizza  Siciliana– (rajčatový základ, sýr, česnek, klobáska, artyčoky, rajčata)',
                        'Menu VII165 Kč\nSport poke bowl - losos gravlax, rýže, edamame (sojové fazole), ředkev, '
                        'červené zelí, nakládaný  \n                       zázvor, okurek, ananas, avokádový dresink, '
                        'zdobené sezamem a jalapeňo papričkou',
                        'Menu VIII165 Kč\nSmažený kuřecí řízek servírovaný s bramborovou kaší a zelným coleslaw '
                        'salátkem'],
            'Pátek': ['Polévka (k menu zdarma)30 Kč\nKvětákový krém',
                      'Menu I160 Kč\nChilli con Carne s mletým masem a červenými fazolemi, jasmínová rýže, '
                      'kysaná smetana',
                      'Menu II170 Kč\nKuřecí steak zapečený rajčaty a mozzarellou, lehká tomatová omáčka, bramborové '
                      'hranolky \n              zdobené lístky rukoly',
                      'Menu III185 Kč\nVepřový steak z kotlety, gorgonzolová omáčka s vlašskými ořechy, '
                      'domácí americké brambory',
                      'Menu IV210 Kč\nSport Cafe ciabatta burger - filírovaný kuřecí steak v rozpečené ciabatte, '
                      'slaninová majonéza \n             nakládaná zelenina, cibulová marmeláda, batátové hranolky, '
                      'tatarská omáčka',
                      'Menu V165 Kč\nSmažený sýr, bramborové hranolky, zelný coleslaw salátek',
                      'Menu VI165 Kč\nø32 cm Pizza  Siciliana– (rajčatový základ, sýr, česnek, klobáska, artyčoky, '
                      'rajčata)',
                      'Menu VII165 Kč\nFIT Sport poke bowl- losos gravlax, rýže, edamame (sojové fazole), ředkev, '
                      'červené zelí, nakládaný  \n                       zázvor, okurek, ananas, avokádový dresink, '
                      'zdobené sezamem a jalapeňo papričkou',
                      'Menu VIII165 Kč\nSmažený kuřecí řízek servírovaný s bramborovou kaší a zelným coleslaw salátkem']
        }
        
        self.assertEqual(expected_value, sport_cafe.menu)
    
    def test_name_property(self):
        sport_cafe = SportCafe("https://www.sport-cafe.cz/#tydenni-menu", "Sport Café")
        self.assertEqual(sport_cafe.name, "Sport Café")


if __name__ == '__main__':
    unittest.main()
