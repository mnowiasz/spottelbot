# Changes #

## 2018-07-04 
### 0.1.1
- Fixed a hidden bug: The bot was only running for one hour before raising an
  exception. Found the solution here: https://stackoverflow.com/questions/48883731/refresh-token-spotipy
- /last 5-1 was possible, but causing a telegram exception. Now it's illegal

### 0.1.0
- Initial release
