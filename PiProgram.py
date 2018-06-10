import pygame, sys, time
from pygame.locals import *
import numpy as np

CompletedWidth = 700
CompletedHeight = 700
CurrentWidth = 500

WindowWidth = CompletedWidth + CurrentWidth
WindowHeight = CompletedHeight

Black = (0  ,0  ,0  )
White = (255,255,255)
Red   = (255,0  ,0  )
Green = (0  ,255,0  )

FPS =  60

AnimationDuration = FPS / 4

NoPerLine = 28

StartingHealth = 3 
HeartSpacing = 10

LegalInputs = [49,50,51,52,53,54,55,56,57,48,46]
CorrespondingValues = ["1","2","3","4","5","6","7","8","9","0","."]

pi = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748"

EmptyHeart = pygame.image.load("EmptyHeart.png")
ImgWidth, ImgHeight = EmptyHeart.get_rect().size
FullHeart = pygame.image.load("FullHeart.png")



class PiTrainer:
	def __init__(self):
		pygame.init()

		self.DisplayScreen = pygame.display.set_mode((WindowWidth,WindowHeight))

		self.clock = pygame.time.Clock()

		self.initGame()

	def initGame(self):
		self.running = True
		self.playing = True 
		self.currentDigit = 0
		self.allCorrect = "3"
		self.currentRectColor = Black
		self.animationTimer = 0
		self.health = StartingHealth - 1

		self.Font = pygame.font.SysFont("courier", 42, bold=True)
		self.CurrentFont = pygame.font.SysFont("courier", 700, bold=True)
		self.TotalFont = pygame.font.SysFont("courier", 100, bold=True)
		self.LosingFont = pygame.font.SysFont("courier", 130, bold=True)


	def writeCorrectDigits(self):
		allDrawingRects = []
		noOfLines = (self.currentDigit / NoPerLine) + 1
		currentLine = 0
		for startNumber in range(0, self.currentDigit, NoPerLine):
			currentLine += 1
			if currentLine != noOfLines:
				allDrawingRects.append(self.Font.render("%s" %(self.allCorrect[startNumber : startNumber + NoPerLine]), True, White))
			else:
				allDrawingRects.append(self.Font.render("%s" %(self.allCorrect[startNumber : -1]), True, White))

		for x in range(len(allDrawingRects)):
			self.DisplayScreen.blit(allDrawingRects[x], (1, x * 32))

	def writeCurrentDigit(self):
		if self.currentDigit == 0:
			currentDigitRect = self.CurrentFont.render(" ", True, White)
		else:
			currentDigitRect = self.CurrentFont.render("%s" %(pi[self.currentDigit - 1]), True, White)
		self.DisplayScreen.blit(currentDigitRect, (CompletedWidth + 40, -20))

	def writeTotalCounter(self):
		totalDigitRect = self.TotalFont.render("%s" %(self.currentDigit), True, White)
		self.DisplayScreen.blit(totalDigitRect, (CompletedWidth, WindowHeight - 100))

	def drawHealthImages(self):
		for x in range(StartingHealth):
			if x <= self.health:
				currentImage = FullHeart
			else:
				currentImage = EmptyHeart

			self.DisplayScreen.blit(currentImage, ((WindowWidth - HeartSpacing - ImgWidth) - x * (HeartSpacing + ImgWidth), HeartSpacing))

	def drawLosingScreen(self):
		losingRect = self.LosingFont.render("You Recited %s" %(self.currentDigit), True, White)
		losingRect2 = self.LosingFont.render("Digits Of Pi", True, White)
		rectangle = losingRect.get_rect()
		rectangle2 = losingRect2.get_rect()
		self.DisplayScreen.blit(losingRect, ((WindowWidth / 2) - (rectangle[2] / 2), (WindowHeight / 2) - rectangle[3]))
		self.DisplayScreen.blit(losingRect2, ((WindowWidth / 2) - (rectangle2[2] / 2), (WindowHeight / 2)))

	def checkInput(self, digitEntered):		
		if pi[self.currentDigit] == digitEntered:
			self.currentDigit += 1
			self.allCorrect += pi[self.currentDigit]
			self.currentRectColor = Green
		else: 
			self.currentRectColor = Red
			self.health -= 1 
			
		self.animationTimer += AnimationDuration

	def terminate(self):
		pygame.quit()
		sys.exit()

	def run(self):
		while self.running:
			if self.playing:
				for event in pygame.event.get():
					if event.type == QUIT:
						self.terminate()
					if event.type == KEYDOWN:
						if event.key == K_ESCAPE:
							self.terminate()
						elif event.key == K_BACKSPACE:
							self.initGame()
						for inputValue in LegalInputs:
							if event.key == inputValue:
								self.checkInput(CorrespondingValues[LegalInputs.index(inputValue)])

				if self.animationTimer > 0:
					self.animationTimer -= 1
				elif self.animationTimer < 0:
					self.animationTimer += 1
				else:
					self.currentRectColor = Black

				if self.health < 0 and self.animationTimer == 0:
					self.playing = False

				self.DisplayScreen.fill(Black)
				pygame.draw.rect(self.DisplayScreen, self.currentRectColor, (CompletedWidth, 0, CompletedWidth, WindowHeight))
				self.writeCorrectDigits()
				self.writeCurrentDigit()
				self.writeTotalCounter()
				self.drawHealthImages()
				pygame.display.update()
				self.clock.tick(FPS)
			else:
				for event in pygame.event.get():
					if event.type == QUIT:
						self.terminate()
					if event.type == KEYDOWN:
						if event.key == K_ESCAPE:
							self.terminate()
						else:
							self.initGame()

				self.DisplayScreen.fill(Red)
				self.drawLosingScreen()
				pygame.display.update()
				self.clock.tick(FPS)

if __name__ == '__main__':
	PiTrainer().run()