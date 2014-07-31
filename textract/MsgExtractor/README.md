msg-extractor
=============

Extracts emails and attachments saved in Microsoft Outlook's .msg files

The python script ExtractMsg.py automates the extraction of key email data (from, to, cc, date, subject, body) and the email's attachments.

To use it
```
  python ExtractMsg.py example.msg
```

This will produce a new folder named according to the date, time and subject of the message (for example "2013-07-24_0915 Example").  The email itself can be found inside the new folder along with the attachments.  As of version 0.2, it is capable of extracting both ASCII and Unicode data.

The script uses <a href="http://www.decalage.info/python/olefileio">Philippe Lagadec's Python module</a> that reads Microsoft OLE2 files (also called Structured Storage, Compound File Binary Format or Compound Document File Format).  This is the underlying format of Outlook's .msg files.  This library currently supports up to Python 2.7. 

The script was built using <a href="http://www.fileformat.info/format/outlookmsg/index.htm">Peter Fiskerstrand's documentation of the .msg format</a>.  <a href="http://www.dimastr.com/redemption/utils.htm">Redemption's discussion of the different property types used within Extended MAPI</a> was also useful.  For future reference, I note that Microsoft have opened up <a href="http://msdn.microsoft.com/en-us/library/cc463912%28v=exchg.80%29.aspx">their documentation of the file format</a>.

There are at least two major issues with version 0.2.  The first is that .msg files can be embedded in .msg files---the script doesn't like them at all and will dump a 'raw' directory instead of the normal output.  This directory will contain all you need from the email, but in a less-than-ideal form.  The second issue is that the script cannot extract the date of sent emails (as opposed to received emails).

If you are having difficulty with a specific file, or would like to extract more than is currently automated, then the --raw flag may be useful:
```
  python ExtractMsg.py --raw example.msg
```


If you have any questions feel free to contact me, Matthew Walker, at mattgwwalker at gmail.com.

