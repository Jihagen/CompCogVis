This Repo implements a Dataset Class transforming images into representations akin to infant visual perception. 
---
The two transformations implemented represent the low visual acuity which develops over the first 12 months of a newborn and the color sensitivity which starts with low sensitivity to only reddish hues, integrating greens followed by yellow and finally blues to almost adult vision over the course of the first year. 
The acuity is implemented via a linear scale as provided in the paper XXX. 
The color sensitivity was manually experimented with following a rough guide from multiple sources including those mentioned below. 
Month 0-1
    Primarily grayscale with a slight ability to perceive red
    Color transformation: Convert image to grayscale, then add a very subtle red tint

Month 2-3
    Beginning to perceive red and green
    Color transformation: Start with grayscale, then gradually introduce red and green hues while keeping other colors muted

Month 4-5
    Increasing sensitivity to red, green, and yellow
    Color transformation: Introduce red, green, and yellow more prominently. Other colors should still be muted but starting to emerge

Month 6-7
    Full color spectrum becomes visible, but not as vivid as adult vision
    Color transformation: Include all colors, but at reduced saturation (about 60-70% of full color)

Month 8-9
    Color vision continues to refine, improved ability to distinguish similar colors
    Color transformation: Increase color saturation to about 80-90% of full color. Enhance contrast between similar colors slightly

Month 10-12
    Color vision is well-developed, though still refining
    Color transformation: Color close to adult vision, about 95% saturation



- Skelton AE, Maule J, Franklin A. Infant color perception: Insight into perceptual development. Child Dev Perspect. 2022 Jun;16(2):90-95. doi: 10.1111/cdep.12447; Epub 2022 Mar 21. PMID: 35915666; PMCID: PMC9314692.



