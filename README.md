# facebook-insight
- Visualize location of pictures of Facebook personal album.
- This is a completely client side app, your data will not be stored anywhere
- Did it for personal use only, so please forgive various blemishes.
- Example : https://bordoray.github.io/facebook-insight/

![PreviewGlobe](https://github.com/bordoray/facebook-insight/blob/main/fbinsight_Globe.gif?raw=true)

![Preview](https://user-images.githubusercontent.com/26103833/182764358-2f4a8800-647e-44e2-8be0-7502d4613af6.png)

## One shot use (client side, planisphere only)
### How to open
- Download fb_api/index.php
- Put it on a server
- Visualize on browser related to web server

### How to use
- Get and copy facebook token <a href="https://developers.facebook.com/tools/explorer/?method=GET&path=me%3Ffields%3Did%2Cname&version=v2.11" target="_blank">here</a>
- Paste access token
- Click on visualize and wait less than one minute, map will appear once process finished.
(Map First display extent is in Japan)

## Permanent use (need long process)
- Clone repository
- Run python command to generate your data
```
cd fb_api
python3 get_fb_data.py
## pics download will take a while, about 100 pics / minute
```
- move `rlinsight_data.js` produced in `fb_api` directory to overwrite `rlinsight_data.js` in `json` directory
- open `index.html` and explore
