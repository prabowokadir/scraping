# scraping

Tips and trick:
1. Always check the target website's accepatable policy to see if accessing the website with automated tools is a violation of its terms of use.
2. urllib accessed the website similarly when open the browser, instead of rendering the content visually it shows the source code as text.
3. Regular expressions or regexes are pattern that can be used to search for text within a string.
    a. Pattern "." used to match one character except newline. For example "a.b" can come from "acb", "a3b", "a@b", etc.
    b. Pattern "*" used to match zero or more character based on the previous element. For example "a*b" can come from "b", "ab", "aab", "aaab", etc.
    c. Pattern "?" have two different function i.e
        * Greedy vs. non-greedy, if "?" used after "*" or "+" then it becomes non-greedy. For example "a.*b" from string "aabacb" then it will be "aab".
        * Zero or one, if it's used after character or group then it will match zero or one based on the element before it. For example "a?b" can be "b" or "ab".