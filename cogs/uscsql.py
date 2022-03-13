import sqlite3
import discord
import sys
from discord.ext import commands, tasks
import functools
import os.path
import datetime
import time
from selenium import webdriver
from PIL import Image
import pyautogui
import pygetwindow


class USCSQL (commands.Cog):
    def __init__(self, client):
        self.client = client

    cwd=os.getcwd() # cwd is the current working dir, where it is looking for the table
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # this is the dir where the table is
    db_path = os.path.join(BASE_DIR, "usctt.sqlite") # set the absolute path to the table
    conn = sqlite3.connect(db_path)

    # conn = sqlite3.connect("usctt.sqlite")
    c = conn.cursor()

    @commands.Cog.listener()
    async def on_ready(self):
        print("SQL Database is online.")

    @commands.command()
    async def sqlping(self, ctx):
        await ctx.send("SQLPong!")

    @commands.command()
    async def username(self, ctx, username):
        # con = sqlite3.connect('usctt.sqlite')
        cwd = os.getcwd()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "usctt.sqlite")
        con = sqlite3.connect(db_path)
        c = con.cursor()
        c.execute(f"SELECT * FROM usctt WHERE discordid = {ctx.author.id}")

        # c.execute(f"INSERT INTO usctt VALUES ({ctx.author.id}, '{username}')")
        if c.fetchone() is None:
            c.execute(f"INSERT INTO usctt VALUES ({ctx.author.id}, '{username}', NULL)")
            await ctx.send("Username has been added to database")
        else:
            c.execute(f"UPDATE usctt SET username = '{username}' WHERE discordid = {ctx.author.id}")
            await ctx.send("Username has been updated")
            
        # c.execute(f"SELECT * FROM usctt WHERE discordid = {ctx.author.id}")
        # if (ctx.author.id == 0):
        #     await ctx.send("Access restricted.")
        # else:        #     if c.fetchone() is None:
        #         c.execute(f"INSERT INTO usctt VALUES ({ctx.author.id}, {username})")
        #         await ctx.send("Username has been added to database")
        #     else:
        #         await ctx.send("You're already in the database!")
        con.commit()
        con.close()

    # @commands.command()
    # async def check(self, ctx):
    #     cwd = os.getcwd()
    #     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #     db_path = os.path.join(BASE_DIR, "usctt.sqlite")
    #     con = sqlite3.connect(db_path)
    #     c = con.cursor()
    #
    #     c.execute(f"SELECT * FROM usctt WHERE discordid = {ctx.author.id}")
    #
    #     if c.fetchone() is None:
    #         await ctx.send(f"{ctx.author.mention} has no data!")
    #     else:
    #         c.execute(f"SELECT username FROM usctt WHERE discordid = {ctx.author.id}")
    #         testname = functools.reduce(lambda sub, ele: sub * 10 + ele, c.fetchone())
    #         await ctx.send(f"{ctx.author.mention} has a username of {testname}")
    #     con.commit()
    #     con.close()

    @commands.command()
    async def password(self, ctx, password):
        cwd = os.getcwd()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "usctt.sqlite")
        con = sqlite3.connect(db_path)
        c = con.cursor()
        c.execute(f"SELECT * FROM usctt WHERE discordid = {ctx.author.id}")
        if c.fetchone() is None:
            c.execute(f"INSERT INTO usctt VALUES ({ctx.author.id}, NULL, '{password}')")
            await ctx.send("Password has been added to database")
        else:
            c.execute(f"UPDATE usctt SET password = '{password}' WHERE discordid = {ctx.author.id}")
            await ctx.send("Password has been updated")
        con.commit()
        con.close()

    @commands.command()
    async def run(self, ctx):
        await ctx.send("Make sure to accept 2FA!")
        
        cwd = os.getcwd()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "usctt.sqlite")
        con = sqlite3.connect(db_path)
        c = con.cursor()

        c.execute(f"SELECT * FROM usctt WHERE discordid = {ctx.author.id}")
        if c.fetchone() is None:
            await ctx.send("You are not in the database! Please use the username and password commands.")
        else:
            c.execute(f"SELECT username FROM usctt WHERE discordid = {ctx.author.id}")
            run_username = functools.reduce(lambda sub, ele: sub * 10 + ele, c.fetchone())
            c.execute(f"SELECT password FROM usctt WHERE discordid = {ctx.author.id}")
            run_password = functools.reduce(lambda sub, ele: sub * 10 + ele, c.fetchone())

            def startBot(run_username, run_password, url, path):

                # giving the path of chromedriver to selenium webdriver
                driver = webdriver.Chrome(path)

                # opening the website in chrome.
                driver.get(url)
                print("Reached Trojan Check")
                driver.implicitly_wait(20)
                # time.sleep(2)

                driver.find_element_by_class_name("button-wrapper").click()
                driver.implicitly_wait(20)
                # time.sleep(3)
                # find the id or name or class of
                # username by inspecting on username input
                driver.find_element_by_name("j_username").send_keys(run_username)

                # find the password by inspecting on password input
                driver.find_element_by_name("j_password").send_keys(run_password)
                driver.implicitly_wait(60)
                # time.sleep(3)

                # Process to start assessment
                # driver.find_element_by_name("_eventId_proceed").click()
                # time.sleep(3)

                # Continue button
                driver.find_element_by_class_name(
                    "mat-focus-indicator.submit-button.btn-next.mat-button.mat-button-base.mat-accent").click()
                print("Continue button")
                driver.implicitly_wait(60)
                # time.sleep(3)
                # Begin wellness assessment
                driver.find_element_by_class_name(
                    "mat-focus-indicator.mat-flat-button.mat-button-base.btn-begin-assessment").click()
                driver.implicitly_wait(20)
                print("Begin button")
                # time.sleep(3)
                # Start Screening
                driver.find_element_by_class_name(
                    "mat-focus-indicator.btn-assessment-start.mat-flat-button.mat-button-base").click()
                driver.implicitly_wait(20)
                print("start screening")
                # time.sleep(3)

                # No and no questions, then next
                # Are you currently required to isolate due to a COVID-19 infection?
                driver.find_element_by_id("mat-button-toggle-2").click()
                driver.find_element_by_class_name(
                    "mat-focus-indicator.btn-next.mat-flat-button.mat-button-base").click()

                # Last page of No's
                driver.implicitly_wait(20)
                # time.sleep(3)
                driver.find_element_by_id("mat-button-toggle-11").click()
                driver.find_element_by_id("mat-button-toggle-13").click()
                driver.find_element_by_id("mat-button-toggle-15").click()
                driver.find_element_by_id("mat-button-toggle-17").click()
                driver.find_element_by_id("mat-button-toggle-19").click()
                driver.find_element_by_id("mat-button-toggle-21").click()
                driver.find_element_by_id("mat-button-toggle-23").click()
                driver.find_element_by_class_name(
                    "mat-focus-indicator.btn-next.mat-flat-button.mat-button-base").click()

                # Verify responses
                driver.implicitly_wait(20)
                # time.sleep(3)
                driver.find_element_by_class_name("mat-checkbox-inner-container").click()
                driver.find_element_by_class_name(
                    "mat-focus-indicator.btn-submit.mat-flat-button.mat-button-base").click()

                # Snap a screenshot of the Trojan Check and save to file
                time.sleep(3)
                ss_path = "C:\\Dev\\PythonPictures\\Trojan_Check_" + run_username + "_" + \
                          (str(datetime.datetime.now()).split(" "))[0] + ".png"

                window = pygetwindow.getWindowsWithTitle('Trojan Check - Google Chrome')[0]
                # print(window)
                x1 = window.left
                y1 = window.top
                height = window.height
                width = window.width

                x2 = x1 + width
                y2 = y1 + height

                pyautogui.screenshot(ss_path)

                im = Image.open(ss_path)
                im = im.crop((x1, y1, x2, y2))
                im.save(ss_path)
                #im.show(ss_path)

                time.sleep(5)
                driver.quit()
                while (True):
                    pass

            url = "https://trojancheck.usc.edu/login"
            path = "C:\Dev\WebDrivers\chromedriver.exe"

            startBot(run_username, run_password, url, path)
            await ctx.send("If you do not receive a result in 15 seconds, try again, because the server might be congested.")
            tries = 0
            while True:
                try:
                    await ctx.send(file=discord.File("C:\\Dev\\PythonPictures\\Trojan_Check_" + run_username + "_" + (str(datetime.datetime.now()).split(" "))[0] + ".png"))
                except:
                    continue
                else:
                    break

            # await ctx.send (f"Your username is {run_username}")

def setup(client):
    client.add_cog(USCSQL(client))