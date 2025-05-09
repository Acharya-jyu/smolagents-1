import os
import time
from dotenv import load_dotenv

# Import E2B sandbox
from e2b import Sandbox

def test_e2b_sandbox():
    # Load environment variables
    load_dotenv()
    
    # Get the E2B API key from environment
    E2B_API_KEY = os.getenv("E2B_API_KEY")
    if not E2B_API_KEY:
        print("E2B_API_KEY not found in environment variables.")
        print("Will try to use the hardcoded key instead.")
        E2B_API_KEY = "e2b_08e7c9cf74f3f671773c7f1600606734c4a071a7"  # Fallback
    
    print(f"Using E2B API key: {E2B_API_KEY[:10]}... (truncated for security)")
    
    try:
        # Create E2B sandbox
        print("Creating E2B sandbox...")
        sandbox = Sandbox(
            template="base",
            api_key=E2B_API_KEY
        )
        print(f"Created E2B sandbox: {sandbox}")
        
        # Check if the sandbox is running
        print(f"Sandbox is running: {sandbox.is_running()}")
        
        # Get sandbox information
        try:
            info = sandbox.get_info()
            print(f"Sandbox info: {info}")
        except Exception as e:
            print(f"Error getting sandbox info: {e}")
        
        # Test working with files
        try:
            print("\nTesting file operations:")
            # Check if 'files' attribute exists
            if hasattr(sandbox, "files"):
                # Write a test Python file
                test_file_content = """
print("Hello from E2B sandbox file!")
import os
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())
"""
                sandbox.files.write("/tmp/test.py", test_file_content)
                print("File written successfully")
                
                # Read the file back
                content = sandbox.files.read("/tmp/test.py")
                print(f"File content: {content}")
                
                # List files in a directory
                files = sandbox.files.list("/tmp")
                print(f"Files in /tmp: {files}")
            else:
                print("'files' attribute not found on sandbox")
        except Exception as e:
            print(f"Error with file operations: {e}")
        
        # Test running commands
        try:
            print("\nTesting command execution:")
            # Check if 'commands' attribute exists
            if hasattr(sandbox, "commands"):
                # Execute a simple Python command
                result = sandbox.commands.python(["-c", "print('Hello from E2B sandbox command!')"])
                print(f"Python command result: {result}")
                
                # Execute a system command
                result = sandbox.commands.exec(["ls", "-la", "/tmp"])
                print(f"System command result: {result}")
                
                # Run the Python file we created earlier
                result = sandbox.commands.python(["/tmp/test.py"])
                print(f"Python file execution result: {result}")
            else:
                print("'commands' attribute not found on sandbox")
        except Exception as e:
            print(f"Error executing commands: {e}")
        
        # Test PTY (terminal) if available
        try:
            print("\nTesting PTY (terminal):")
            if hasattr(sandbox, "pty"):
                # Start a terminal session
                terminal = sandbox.pty.start()
                print(f"Terminal started: {terminal}")
                
                # Write a command to the terminal
                terminal.write("python -c \"print('Hello from PTY terminal!')\"")
                time.sleep(1)  # Wait for command to execute
                
                # Read the output
                output = terminal.read()
                print(f"Terminal output: {output}")
                
                # Close the terminal
                terminal.kill()
            else:
                print("'pty' attribute not found on sandbox")
        except Exception as e:
            print(f"Error with PTY operations: {e}")
        
        # Clean up the sandbox when done
        print("\nCleaning up sandbox...")
        if hasattr(sandbox, "kill"):
            sandbox.kill()
            print("Sandbox killed with .kill()")
        else:
            print("No kill method found - sandbox may continue running")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nPlease check E2B documentation for correct usage")

if __name__ == "__main__":
    test_e2b_sandbox()