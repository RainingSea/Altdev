import os
import subprocess
import sys
import time


def install_package(package_name):
    """Install the missing package."""
    print(f"Installing missing package: {package_name}")
    try:
        # using subprocess to install package while running project
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            timeout=20,  # timeout setting
            check=True,  # throw CalledProcessError error
        )
    except subprocess.TimeoutExpired:
        print(f"Installation of {package_name} timed out after 60 seconds.")
        return "INS_E"
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}. Error: {e}")
        return "INS_E"
    else:
        if result.returncode == 0:
            print(f"{package_name} installed successfully.")
        return "INS_S"


def run_main_py(directory):
    """Execute the main.py file from the specified directory."""
    main_py_path = os.path.join(directory, "main.py")
    try:
        # Execute the main.py script with a timeout
        process = subprocess.Popen(
            [sys.executable, main_py_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("1")
        try:
            # Wait for a specified time or until the process completes
            stdout, stderr = process.communicate(timeout=2)  # Adjust timeout as needed
            normal_exit = True
        except subprocess.TimeoutExpired:
            # Process is still running after timeout, terminate it
            process.terminate()
            stdout, stderr = (
                process.communicate()
            )  # Fetch any remaining output after termination
            normal_exit = False

        # Decode output and error
        stdout = stdout.decode()
        stderr = stderr.decode()

        if normal_exit and process.returncode == 0:
            print("Program executed successfully with no errors.")
            return "SUCCESS", None
        elif not normal_exit:
            print(
                "Process terminated due to timeout, which is considered as normal execution."
            )
            return "SUCCESS", None
        else:
            print(f"Error: {stderr}")

            if "No module named" in stderr:
                missing_package = (
                    stderr.split("No module named")[-1].strip().replace("'", "")
                )
                return "IMPORT_ERROR", missing_package
            else:
                return "OTHER_ERROR", stderr

    except Exception as e:
        return "OTHER_ERROR", str(e)


def main():

    directory = ".../code"
    i = 0
    while i < 1:
        result, data = run_main_py(directory)

        if result == "SUCCESS":
            print("Execution completed successfully.")
            break
        elif result == "IMPORT_ERROR":
            install_package(data)
            print("Restarting the execution after installing the missing package.")
        elif result == "OTHER_ERROR":
            print(f"An error occurred: {data}")
            break
        i = i + 1


if __name__ == "__main__":
    main()
