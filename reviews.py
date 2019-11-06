import csv
import argparse
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

parser = argparse.ArgumentParser()
parser.add_argument("-link")
args = parser.parse_args()

reviewList = []
class ReviewInfo:
    def __init__(self, comment, commentLink, rating, ratingDate, profileName, profileLink):
        self.comment = comment
        self.commentLink = commentLink
        self.rating = rating
        self.ratingDate = ratingDate
        self.profileName = profileName
        self.profileLink = profileLink

    def to_dict(self):
        return {
            'comment': self.comment,
            'commentLink': self.commentLink,
            'rating': self.rating,
            'ratingDate': self.ratingDate,
            'profileName': self.profileName,
            'profileLink': self.profileLink,
        }

def getYelpReviews(yelpLink):
    driver = webdriver.Firefox()
    driver.get(yelpLink)

    #WHILE NEXT BUTTON FOR MORE REVIEWS IS THERE WE WILL CONTINUE GETTING REVIEWS
    nextFound = True
    while nextFound:

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='lemon--div__373c0__1mboc sidebarActionsHoverTarget__373c0__2kfhE arrange__373c0__UHqhV gutter-12__373c0__3kguh layout-stack-small__373c0__3cHex border-color--default__373c0__2oFDT']")))
        reviews = driver.find_elements_by_xpath("//div[@class='lemon--div__373c0__1mboc sidebarActionsHoverTarget__373c0__2kfhE arrange__373c0__UHqhV gutter-12__373c0__3kguh layout-stack-small__373c0__3cHex border-color--default__373c0__2oFDT']")

        for review in reviews:
            theReview = ReviewInfo('', '', '', '', '', '')

            #GET RATING
            ratingDiv = review.find_element_by_xpath(".//div[@class='lemon--div__373c0__1mboc arrange__373c0__UHqhV gutter-6__373c0__zqA5A vertical-align-middle__373c0__2TQsQ border-color--default__373c0__2oFDT']")
            rating = ratingDiv.find_element_by_xpath(".//span[@class='lemon--span__373c0__3997G display--inline__373c0__1DbOG border-color--default__373c0__2oFDT']")
            theReview.rating = rating.find_element_by_tag_name('div').get_attribute('aria-label').replace(" star rating", "")

            #GET DATE OF RATING
            dateOfReview = review.find_element_by_xpath(".//span[@class='lemon--span__373c0__3997G text__373c0__2pB8f text-color--mid__373c0__3G312 text-align--left__373c0__2pnx_']")
            theReview.ratingDate = dateOfReview.text

            #GET COMMENT
            commentParagraph = review.find_element_by_xpath(".//p[@class='lemon--p__373c0__3Qnnj text__373c0__2pB8f comment__373c0__3EKjH text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_']")
            theReview.comment = commentParagraph.text

            #GET PROFILE NAME AND LINK TO PROFILE
            profileDiv = review.find_element_by_xpath(".//div[@class='lemon--div__373c0__1mboc user-passport-info border-color--default__373c0__2oFDT']")
            profileLink = profileDiv.find_element_by_tag_name('a').get_attribute('href')
            profileName = profileDiv.find_element_by_tag_name('span').text
            theReview.profileLink = profileLink
            theReview.profileName = profileName

            #GET LINK TO COMMENT
            review.find_element_by_xpath(".//p[contains(text(),'Share review')]").click()
            time.sleep(1)
            linkDiv = driver.find_element_by_xpath(".//div[@class='lemon--div__373c0__1mboc pseudo-input-field-holder__373c0__3HUEO border-color--default__373c0__2oFDT']")
            commentLink = linkDiv.find_element_by_tag_name('input').get_attribute('value')
            theReview.commentLink = commentLink

            #ADD REVIEW TO LIST
            reviewList.append(theReview)

            #CLOSE SHARE POP-UP
            driver.find_element_by_xpath(".//a[@class='lemon--a__373c0__IEZFH dismiss-link__373c0__3xvNi inherit-size__373c0__2Q1RX light__373c0__2qT0e']").click()

        #CHECK IF NEXT PAGE FOR MORE COMMENTS EXISTS - IF IT DOES NOT WE WILL STOP GETTING REVIEWS
        try:
            nextBtn = driver.find_element_by_xpath("//div[@class='lemon--div__373c0__1mboc navigation-button-text__373c0__38ysY u-space-l2 border-color--default__373c0__2oFDT']")
            nextBtn.find_element_by_tag_name('span').click()
        except NoSuchElementException:
            nextFound = False
            print("No more next found")
            
    driver.close()

def createCSV(yelpLink):
    with open('reviews.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Comment', 'CommentLink', 'Rating', 'Rating Date', 'Profile Name', 'Profile Link'])
        x = 1
        for review in reviewList:
            writer.writerow([str(x), review.comment, review.commentLink, review.rating, review.ratingDate, review.profileName, review.profileLink])
            x+=1

if __name__ == '__main__':
    getYelpReviews(args.link)
    createCSV(args.link)