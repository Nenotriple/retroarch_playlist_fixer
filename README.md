<h1 align="center">Retroarch Playlist Fixer</h1>
<p align="center">Easily redefine Retroarch playlist "path" and "db_name"</p>


<p align="center">
  <img src="https://github.com/Nenotriple/retroarch_playlist_fixer/assets/70049990/42a341e5-e967-4c9c-ab3d-edcdc3e7903c" alt="app_cover">
</p>


📜 Description:
-------------
This Python script allows you to redefine the `path` and `db_name` in your JSON formatted .lpl files.
It creates a backup of the original file before making any changes.

`path` (Rom Path) is edited by only changing the folder path, it does not change the filename or file extension.

`db_name` will use the same name as the selected `.lpl` file.


📝 Usage:
-------------
1. Select the `.lpl` playlist file you want to edit.
2. Browse or enter the new/current rom path.
3. Click `Run!`

Example:
 - Playlist File: `C:/retroarch/playlists/Atari - 2600.lpl`
 - Rom Path: `C:/roms/Atari - 2600/`


📂 Folder Structure:
-------------

Only use with roms in a base folder like this👇
```
System
├── Game 1
├── Game 2
├── Game 3
└── Game 4
```

Do not use with roms in subfolders like this👇
```
System
├── A
│   ├── Game 1
│   └── Game 2
└── B
    ├── Game 1
    └── Game 2
```
*Using this app with a playlist that's setup with subfolders will break the playlist!!!*
