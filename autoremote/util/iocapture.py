import sys,StringIO

class IOCapture():
    @classmethod
    def startCapture(self):
        if hasattr(self, "capturing") and self.capturing:
            return False

        self.capturing = True
        self.strListeners = []

        self.saveStdout = sys.stdout
        self.saveStderr = sys.stderr
        self.stdout = StringIO.StringIO()
        self.stderr = StringIO.StringIO()

        IOCapture.wrapFileWithFunc(self.stdout,IOCapture.dispatchMessageToListeners)
        IOCapture.wrapFileWithFunc(self.stderr,IOCapture.dispatchMessageToListeners)

        sys.stdout = self.stdout
        sys.stderr = self.stderr

    @staticmethod
    def wrapFileWithFunc(file,func):

        oldWriteFunc = file.write

        def logAndPassThrough(message):
            func(message)
            oldWriteFunc(message)

            file.write = logAndPassThrough

            return file
        file.write = logAndPassThrough

    @classmethod
    def dispatchMessageToListeners(self,message):
        for i in range(0,len(self.strListeners)):
            self.strListeners[i] += message


    @classmethod
    def bypassPrint(self,msg):
        self.saveStdout.write(msg)



    @classmethod
    def startListening(self):


        newListener = ""
        self.strListeners.append("")

        return len(self.strListeners)-1

    @classmethod
    def getListener(self,index):
        return self.strListeners[index]

    @classmethod
    def getStOutContents(self):
        return self.stdout.getvalue()

    @classmethod
    def getStErrContents(self):
        return self.stderr.getvalue()

    @classmethod
    def stopCapture(self,passThroughToOriginal=False):
        sys.stderr = self.saveStderr
        sys.stdout = self.saveStdout

        if(passThroughToOriginal):
            if(IOCapture.getStOutContents()):
                print >>sys.stdout,IOCapture.getStOutContents()
            if(IOCapture.getStErrContents()):
                print >>sys.stderr,IOCapture.getStErrContents()

        self.stdout.close()
        self.stderr.close()
        self.capturing = False

