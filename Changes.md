# Changes #

## 2018-08-09
### 0.2.4

- Bugfix: /last now shows playlists again
## 2018-07-14
### 0.2.3

- Bugfix: Provide for a rare condition (indicating a problem at spotify's server)
where the track's context (playlist or album) is empty causing an exception
 
## 2018-07-11
### 0.2.2

- Bugfix: Another time/date error, regression introduced in 0.2.1
- Added a default handler for unknown commands

## 2018-07-09
### 0.2.1

- Bugfix: Time/date are now correctly shown in /last
- Mild refactoring (internal methods are now mostly __)

## 2018-07-08
### 0.2.0

- /last now shows when the tracks were played
- Added /reload command (not very useful yet)
- Code cleanup

## 2018-07-04 
### 0.1.1
- Fixed a hidden bug: The bot was only running for one hour before raising an
  exception. Found the solution here: https://stackoverflow.com/questions/48883731/refresh-token-spotipy
- /last 5-1 was possible, but causing a telegram exception. Now it's illegal

### 0.1.0
- Initial release
