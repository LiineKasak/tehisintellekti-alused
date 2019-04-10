import math
import os


class ContentUtil:

    @staticmethod
    def word_filter(w: str) -> bool:
        w = w.strip()
        if len(w) < 4:
            return True
        return False

    @staticmethod
    def read_dir(dir_name: str) -> list:
        cont_l = []
        for fn in os.listdir(dir_name):
            with open(os.path.join(dir_name, fn), encoding="latin-1") as f:
                words = [w.strip()
                         for w in f.read().replace("\n", " ").split(" ")
                         if not ContentUtil.word_filter(w)
                         ]
                cont_l.append(words)
        return cont_l


class BayesSpamFilter:

    def __init__(self):
        ham_l = ContentUtil.read_dir("enron6\\ham")
        spam_l = ContentUtil.read_dir("enron6\\spam")

        n_ham = len(ham_l)
        n_spam = len(spam_l)
        n = n_ham + n_spam
        print(f"Ham nr: {n_ham}\nSpam nr: {n_spam}\n")

        self.p_ham = n_ham / n
        self.p_spam = 1 - self.p_ham

        self.ham_map = self.get_word_map_for_list(ham_l)
        self.spam_map = self.get_word_map_for_list(spam_l)

        self.word_n_ham = sum(self.ham_map.values())
        self.word_n_spam = sum(self.spam_map.values())
        print(f"Words ham: {self.word_n_ham}\nWords spam: {self.word_n_spam}\n")

        self.unique = len(set(list(self.ham_map.keys()) + list(self.spam_map.keys())))
        print(f"Unique: {self.unique}\n")

    @staticmethod
    def get_word_map_for_list(emails: list) -> dict:
        d = {}
        for words in emails:
            for word in words:
                if word not in d:
                    d[word] = 0
                d[word] += 1
        return d

    def word_spam_p(self, word: str) -> float:
        c = 0 if word not in self.spam_map else self.spam_map[word]
        return (c + 1) / (self.word_n_spam + self.unique)

    def word_ham_p(self, word: str) -> float:
        c = 0 if word not in self.ham_map else self.ham_map[word]
        return (c + 1) / (self.word_n_ham + self.unique)

    def is_spam(self, email: str) -> bool:
        ln_h_spam = math.log(self.p_spam)
        ln_h_ham = math.log(self.p_ham)
        for word in email.split():
            if word in self.spam_map or word in self.ham_map:
                ln_h_spam += math.log(self.word_spam_p(word))
                ln_h_ham += math.log(self.word_ham_p(word))
        print(f"Probability logarithm of spam: {ln_h_spam},\nprobability logarithm of not spam: {ln_h_ham}")
        return ln_h_spam > ln_h_ham


email1 = "Subject: cleburne issues daren , with megan gone i just wanted to touch base with you on the status of the enron payments owed to the cleburne plant . the current issues are as follows : november gas sales $ 600 , 377 . 50 october payment to ena for txu pipeline charges $ 108 , 405 . 00 cleburne receivable from enron $ 708 , 782 . 50 less : november gas agency fees ( $ 54 , 000 . 00 ) net cleburne receivable from enron $ 654 , 782 . 50 per my discussions with megan , she stated that about $ 500 k of the $ 600 k nov gas sales was intercompany ( desk to desk ) sales , with the remainder from txu . are we able to settle any intercompany deals now ? are we able to settle with txu ? additionally , you ' ll see that i included the oct txu payment in the receivable owed to cleburne also . this is because i always pay megan based upon the pipeline estimates in michael ' s file , even though they are not finalized until the next month . therefore in my november payment to enron , i paid ena for october ' s estimate , of which megan would have paid the final bill on 12 / 26 / 01 when it was finalized . however , i had to pay the october bill directly last month , even though i had already sent the funds to ena in november . therefore , i essentially paid this bill twice ( once to ena in nov & once to txu in dec ) . i deducted the november agency fees from these receivable totals to show the net amount owed to cleburne . please advise as to the status of these bills . you can reach me at 713 - 853 - 7280 . thanks ."
email2 = "Subject: immediate contract payment . immediate contract payment . our ref : cbn / ird / cbx / 021 / 05 attn : during the auditing and closing of all financial records of the central bank of nigeria ( cbn ) it was discovered from the records of outstanding foreign contractors due for payment with the federal government of nigeria in the year 2005 that your name and company is next on the list of those who will received their fund . i wish to officially notify you that your payment is being processed and will be released to you as soon as you respond to this letter . also note that from the record in our file , your outstanding contract payment is usd $ 85 , 000 , 000 . 00 ( eighty - five million united states dollars ) . kindly re - confirm to me if this is inline with what you have in your record and also re - confirm the information below to enable this office proceed and finalize your fund remittance without further delays . 1 ) your full name . 2 ) phone , fax and mobile # . 3 ) company name , position and address . 4 ) profession , age and marital status . 5 ) copy of drivers license i . d . as soon as the above information are received , your payment will be made available to you via an international certified bank draft , which will be delivered to your doorstep for your confirmation . you should call my direct number as soon as you receive this letter for further discussion and more clarification . also get back to me on this e - mail address ( payment _ info _ 10 @ yahoo . com ) and ensure that you fax me all the details requested to my direct fax number as instructed . best regards , prof . charles c . soludo . executive governor central bank of nigeria ( cbn ) tel : 234 - 1 - 476 - 5017 fax : 234 - 1 - 759 - 0130 website : www . cenbank . org mail sent from webmail service at php - nuke powered site - http : / / yoursite . com"

if __name__ == '__main__':
    b_filter = BayesSpamFilter()

    print("Email 1 is spam: ")
    print(b_filter.is_spam(email1))

    print("\nEmail 2 is spam: ")
    print(b_filter.is_spam(email2))
