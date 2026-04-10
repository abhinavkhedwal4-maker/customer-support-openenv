with open('server/app.py', 'r') as f:
    content = f.read()

old = 'if __name__ == "__main__":\n    uvicorn.run(app, host="0.0.0.0", port=7860)'
new = 'def main():\n    uvicorn.run(app, host="0.0.0.0", port=7860)\n\n\nif __name__ == "__main__":\n    main()'

content = content.replace(old, new)

with open('server/app.py', 'w') as f:
    f.write(content)

print("Done!")