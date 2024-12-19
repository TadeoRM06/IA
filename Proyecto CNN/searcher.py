from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.contrib.search import Search, Filter

SEARCHS = [
    ("volvo xc40", "volvo xc40 2020"),
    ("mazada 3", "mazda 3 2024"),
]

for car, query in SEARCHS:
    results = Search(
        query, filters={"duration": Filter.get_duration("Under 10 minutes")}
    )
    results.get_next_results()
    results.get_next_results()
    print(f"Found {len(results.videos)} videos for {car}")
    i = 0
    for result in results.videos:
        try:
            yt = YouTube(result.watch_url, on_progress_callback=on_progress)
            video = yt.streams.get_highest_resolution()
            print(f"Downloading video {i} for {car}...")
            video.download(output_path=f"src/videos/{car}", filename=f"{car}{i}.mp4")
            i += 1
            print(f"Video for {car} downloaded successfully")
        except:
            print(f"Failed to download video for {car}")