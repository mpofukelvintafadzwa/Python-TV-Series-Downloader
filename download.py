# script by to fetch file from the links, and download it
import urllib2, sys 

class downloadFile():

   def __init__(self, savedir):
      self.savedir = savedir

   def startDownload(self,url,):
      self.filename = url.replace('%20','_').split('/')[-1] # get filename, get last one after split
      self.response = urllib2.urlopen(url); # open file
      print "\nDownloading " + self.filename # alert user what file is currently downloading

      # call function
      self.chunk_read(self.response, self.filename, report_hook=self.chunk_report)  

   # function for progress report, will update the bytes downloaded realtime
   def chunk_report(self, bytes_so_far, chunk_size, total_size):
      percent = float(bytes_so_far) / total_size
      percent = round(percent*100, 2)
      # convert bytes to megabytes and display
      sys.stdout.write("Downloaded %.2f MB of %.2f MB (%0.2f%%)\r" % 
          ((bytes_so_far * (10 ** -6)), (total_size * (10 ** -6)), percent))

      # if total bytes read is equal to total file size, download complete
      if bytes_so_far >= total_size:
         sys.stdout.write('\nFile download completed.\n')

   # to read the file bytes and write(save) to file.
   # change chunk_size to any bytes you want.
   def chunk_read(self, response, filename, chunk_size=8192, report_hook=None):
      # get file size
      # note: some server did not support/supply the response with 'Content-Length',
      # so the program will throw an error, and cannot download the file.
      total_size = self.response.info().getheader('Content-Length').strip() 
      total_size = int(total_size)
      bytes_so_far = 0
      savefile = open(self.savedir + self.filename,'wb') # create output file

      while 1:
         chunk = self.response.read(chunk_size) # read the response in chunks
         if not chunk:
            break

         bytes_so_far += len(chunk) # add the current chunk into the variable, used for progress
         savefile.write(chunk) # read and write the file to local (download)

         if report_hook:
            report_hook(bytes_so_far, chunk_size, total_size)

      return bytes_so_far # return total of bytes for the progress usage
      savefile.close() # close the file