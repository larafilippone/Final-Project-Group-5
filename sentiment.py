from textblob import TextBlob

# Your provided text
text = """
;review_text;review_date;review_title;review_stars;review_specifics
0;Wife wanted a waffle maker with removable plates - did a bunch of research and found & the B&D to be the best value for the money - haven't had a chance to make waffles - yet - but - seems to be a nice little unit over all ....;Reviewed in the United States on January 3, 2024;"5.0 out of 5 stars Another purchase for the wife ...";5.0 out of 5 stars;Size: 3-in-1Color: Silver
1;This is a $20 waffle iron hiding behind a much higher price tag.Out of the box it just wouldn't work right...- the lip of the top and bottom parts weren't the same shape as the griddle plates- the spring mechanism on my BRAND NEW iron wouldn't hold the plates in place, and the bottom one would pull on the top one when opening, and the plate would drop out- waffle pattern is very shallow. To each their own I guess, but I do not like this aspect.- waffle plates are very thin. Even with the electric element having a good shape to it, there was a degree of uneven heat distribution.;Reviewed in the United States on January 1, 2024;"1.0 out of 5 stars Chintzy piece of garbage - not the one it looks like from my youth";1.0 out of 5 stars;Size: 3-in-1Color: Silver
2;I was so excided to see that our 25 year old waffle iron was still madethis was and now is the best waffle maker.;Reviewed in the United States on December 28, 2023;"5.0 out of 5 stars Replaced old one";5.0 out of 5 stars;Size: 3-in-1Color: Silver
3;This thing SUCKS!! I’ll keep this short and sweet:1) It’s so cheaply made that the clips that are supposed to keep the heating trays in do not actually hold them in place. The whole body/frame looks like it’s warped.2) The outside gets SO hot, it’s unsafe. And yes, I’m aware it’s common for waffle makers to get hot. This one is over the top though. What’s worse is that it’s still not hot enough! This leads to issue 3:3) The waffles are so small and thin that they come out dry and rubbery.This thing sucks!!!;Reviewed in the United States on December 27, 2023;"1.0 out of 5 stars Cheap and Dangerous!";1.0 out of 5 stars;Size: 3-in-1Color: Silver
4;Disappointed that the instructions do not fulfill the expectation of good baking.;Reviewed in the United States on December 27, 2023;"2.0 out of 5 stars This product has uneven closing of the waffle plates. Seems broken.";2.0 out of 5 stars;Size: 3-in-1Color: Silver
5;Found flakes of the non stick coating coming off when we opened the box. Several silver spots showing on the grills before we even used it. Very cheap.;Reviewed in the United States on December 25, 2023;"1.0 out of 5 stars Non-stick coating coming off";1.0 out of 5 stars;Size: 3-in-1Color: Silver
6;My original multi waffle maker is over 45 years old and still working love the size and it’s multi functions;Reviewed in the United States on December 25, 2023;"5.0 out of 5 stars Serving sizes and multiple uses";5.0 out of 5 stars;Size: 3-in-1Color: Silver
7;Has removable plates for cleaning. Be sure not to overfill, allow batter to spread out or you will have a mess to clean up. Browned up the waffles nicely.;Reviewed in the United States on December 22, 2023;"5.0 out of 5 stars Waffle maker worked great";5.0 out of 5 stars;Size: 3-in-1Color: Silver
"""

# Split the text into individual reviews
reviews = text.split("\n")[1:-1]  # Exclude the empty first and last elements

# Perform sentiment analysis for each review
for review in reviews:
    review_text = review.split(";")[1]
    analysis = TextBlob(review_text)
    sentiment = "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

    print(f"Review: {review_text}\nSentiment: {sentiment}\n")