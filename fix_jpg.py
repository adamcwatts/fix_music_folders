import os


def jpg_search(file_path):
    jpg = [file for file in os.listdir(file_path) if ('cover' and 'jpg') in file]
    return jpg


def cover_rename(base_dir, jpg_files):
    dir_and_new_album_name = os.path.join(base_dir, 'cover.jpg')
    dir_and_old_album_name = os.path.join(base_dir, jpg_files[0])
    artist_name = dir_and_new_album_name.split('\\')[-3]
    album_name = dir_and_new_album_name.split('\\')[-2]

    if dir_and_new_album_name != dir_and_old_album_name:
        try:
            os.rename(dir_and_old_album_name, dir_and_new_album_name)
            print('\n')
            print(f'{artist_name}: {album_name}')
            print(f'Old Album Cover File Name: {jpg_files[0]}' + "    --------------->   " +
                  f'New Album Cover File Name: cover.jpg')

        except FileExistsError:
            for bad_image in jpg_files:
                if bad_image != 'cover.jpg':
                    try:
                        os.remove(dir_and_old_album_name)
                    except FileNotFoundError:
                        continue
            pass
    else:
        print('\n')
        print(f'{artist_name}: {album_name} : Already Correct')
        # for bad_image in jpg_files:
        #     if bad_image != 'cover.jpg':
        #         try:
        #             os.remove(dir_and_old_album_name)
        #         except FileNotFoundError:
        #             continue
    updated_jpg_files = jpg_search(base_dir)
    for bad_image in updated_jpg_files:
        if bad_image != 'cover.jpg':
            try:
                bad_image_path = os.path.join(base_dir, bad_image)
                os.chmod(bad_image_path, 0o777)  # remove read only attribute
                os.remove(bad_image_path)
                print(f'Deleting {bad_image} in {artist_name}: {album_name}')
            except FileNotFoundError:
                print(f'File Not Found!! : {bad_image}')
                continue


genre_list = [f.path for f in os.scandir(r'D:\FileHistory\adamc\ADAMSPC\Data\Fake_Drive') if f.is_dir()]
for genre in genre_list:
    artist_list = [f.path for f in os.scandir(genre) if f.is_dir()]
    for artist in artist_list:
        album_list = [f.path for f in os.scandir(artist) if f.is_dir()]
        for album in album_list:
            album_cover_flag = False
            disc_flag = False

            # jpg_file = [file for file in os.listdir(album) if ('cover' and 'jpg') in file]
            jpg_file = jpg_search(album)
            disc_list = [f.path for f in os.scandir(album) if f.is_dir()]
            disc_folders = [disc for disc in disc_list if ('cd' or 'disc') in disc.lower()]

            if len(jpg_file) > 0:
                album_cover_flag = True

            if len(disc_folders) > 0:
                disc_flag = True

            if album_cover_flag:
                cover_rename(album, jpg_file)

            if disc_flag:
                for disc in disc_folders:
                    nested_album_flag = False

                    album_and_disc = os.path.join(album, disc)
                    jpg_in_disc = jpg_search(album_and_disc)

                    if len(jpg_in_disc) > 0:
                        nested_album_flag = True

                    if nested_album_flag:
                        cover_rename(album_and_disc, jpg_in_disc)
