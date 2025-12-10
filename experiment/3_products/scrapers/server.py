

'''
Start scraping for provided category and ASINs. 
Server does not know about our local database, it works with category_id and asins.
Once the job is done, we download the result file. 

One worker only. We can use selenium_scraper.py directly.

- Save result to `./output/{request_id}.json`
- Save log to `./output/{request_id}.log`

POST /v1/scrapes/start 

Request: 

{
  "category_id": 1234,
  "site": "amazon",
  "asins": ["B000000000", "B000000001", "B000000002"]
}

Response: 

{
  "message": "Scraping started",
  "status": "accepted",
  "request_id": 98234324
}
'''

'''
Get the status of the scraping process by request id.

GET /v1/scrapes/{request_id}/status

Response: 

- Inprogress (60%)

{
  "message": "Scraping in progress",
  "status": "in_progress",
  "request_id": 98234324,
  "success_count": 50,
  "failed_count": 10,
  "processed_count": 60,
  "total_count": 100
}

- Completed:

{
  "message": "Scraping completed",
  "status": "completed",
  "request_id": 98234324,
  "success_count": 80,
  "failed_count": 20,
  "processed_count": 100,
  "total_count": 100
}
'''

'''
Stop the scraping process by request id.

POST /v1/scrapes/{request_id}/stop

Request:

{
  "reason": "User requested"
}

Response:

{
  "message": "Scraping stopped",
  "code": "stopped",
  "request_id": 98234324,
  "success_count": 50,
  "failed_count": 10,
  "processed_count": 60,
  "total_count": 100
}
'''

'''
File `./output/{request_id}.json` is zipped and downloaded, only when 
status=completed|stopped

GET /v1/scrapes/{request_id}/download

Response:

<Binary file>
'''

'''
Result file format (depends on the status)

{
  "request_id": 98234324,
  "started_at": "2025-01-01 12:00:00",
  "completed_at": "2025-01-02 12:00:00",
  "stopped_at": null,
  "status": "completed",
  "success_count": 80,
  "failed_count": 20,
  "processed_count": 100,
  "total_count": 100,
  "category_id": 177800,
  "category": "4K TVs",
  "products": [
    {
      "url": "https://www.amazon.com/Roku-Smart-2025-Television-Entertainment/dp/B0DWHB9DW4/ref=sr_1_1?crid=3VGY03ZCGWOBG&dib=eyJ2IjoiMSJ9.YarA8OKRWNhaGlfTOxH5md2EB-Pk9ebtyKXVd6-mCbTORuaxbvOCPKMfatdxybhACq7t86-PBJQbDkrGIPEAR3Xb2odUuyBftDylNNIJgeI3C-Hp3vY96JJ3Hx3ZEedeCFu53Jxm4TuqjZ3qR4mfnrUxoN7ij803XjLv11EvxXam3RDGT4uRSFF8iYLfh7l_8FCEAKaFost-A-c42IIxRevcYHyWzKSO4UGnP7TeRgA.PXIMoyQLtYkcmKMucVH6lANpj6ebnZled88gGRzVKKA&dib_tag=se&keywords=4K+TVs&qid=1765013241&sprefix=4k+tvs%2Caps%2C528&sr=8-1",
      "title": "Roku Smart TV 2025 – 43-Inch Select Series, 4K HDR TV – RokuTV with Enhanced Voice Remote – Flat Screen LED Television with Wi-Fi for Streaming Live Local News, Sports, Family Entertainment",
      "price": "VND310,784",
      "attributes": {
        ...
      }
    }
  ]
}
'''

'''

Use 1 of 3 ways to extract the log file by request id.
- By line number range. If to is not provided, return all lines after from.
- Tail the log file.
- Grep the log file (line by line). 
  Also return line count for each grep result

GET /v1/scrapes/{request_id}/logs?tail=1000&grep=<regex>&from=1000&to=2000


Response:

<Log file content>
'''
