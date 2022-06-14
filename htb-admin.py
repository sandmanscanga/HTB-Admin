"""Module for utilizing the HackTheBox API for machine management"""
import os
import sys
import time

from hackthebox import HTBClient
import netifaces as ni


class MultipleMachinesFound(Exception):

    def __init__(self, query, machines):
        self.query = query
        self.machines = machines

    def __str__(self):
        return f"Multiple machines found for search: {self.query}"

    def __iter__(self):
        for machine in self.machines:
            yield machine.name


class Client:
    """HackTheBox API Client"""

    def __init__(self, token_path):
        token = self.get_token(token_path)
        self.client = HTBClient(app_token=token)

    def search(self, query):
        """Searches HackTheBox API for machine given a search query"""

        return self.client.search(query)

    def start(self, machine):
        """Starts an instance of the machine given a machine name"""

        try:
            machine.spawn()
        except KeyError:
            pass
        except Exception as error:
            if "You must stop your active machine" in str(error):
                return 1
            else:
                raise error
        
        return 0

    def info(self):
        """Gets currently active machine information"""

        return self.client.get_active_machine()

    def stop(self):
        """Stops the currently active machine"""

        machine = self.client.get_active_machine()
        if machine is not None:
            machine_name = machine.machine.name
            machine.stop()
            return machine_name

    def reset(self):
        """Resets the currently active machine"""

        machine = self.client.get_active_machine()
        if machine is not None:
            machine_name = machine.machine.name
            try:
                machine.reset()
            except KeyError:
                pass

            return machine_name

    def submit(self, flag, difficulty):
        """Submits a flag to the given machine"""

        machine = self.client.get_active_machine()
        if machine:
            machine_name = machine.machine.name
            message = machine.machine.submit(flag, difficulty)
            return machine_name, message

    def target(self):
        """Gets the currently active machine's IP address"""

        machine = self.client.get_active_machine()
        if machine:
            return machine.ip

    @staticmethod
    def get_local_ip():
        """Gets the local IP address of the tun0 adapter"""

        try:
            address = ni.ifaddresses("tun0")[ni.AF_INET][0]["addr"]
        except ValueError:
            address = None

        return address

    @staticmethod
    def get_token(token_path=None):
        """Gets the HackTheBox API token"""

        if token_path is None:
            token = os.environ.get("HTB_TOKEN", None)
            if token is None:
                error = "[-] Could not find HackTheBox API token"
                raise Exception(error)
        else:
            with open(token_path, "r") as file:
                token = file.read().strip()

        return token


def main(args):
    client = Client(args.token_path)
    if args.query:
        result = client.search(args.query)
        if len(result.machines) == 1:
            machine = result.machines[0]
            print(f"{machine.name} -> {machine.id}")
        elif len(result.machines) > 1:
            for machine in result.machines:
                print(f"{machine.name} -> {machine.id}")
        else:
            raise Exception(f"No machines found for query: {args.query}")
    elif args.start:
        result = client.search(args.start)
        if len(result.machines) == 1:
            machine = result.machines[0]
            result = client.start(machine)
            if result == 0:
                start_time = time.perf_counter()
                print(f"Started instance: {machine.name}")
                print("The machine takes time to start up completely")
                print("Please wait...")
                total = 300
                address = None
                for second in range(total):
                    time.sleep(1)
                    try:
                        address = client.target()
                    except StopIteration:
                        pass
                    else:
                        if address is not None:
                            end_time = time.perf_counter()
                            elapsed = round(end_time - start_time, 2)
                            print(f"Elapsed time: {elapsed} seconds")
                            print(f"Finished: {address}")
                            break
                else:
                    print(f"There was a problem starting: {machine}")
            elif result == 1:
                print("There is a machine that is already active")
        elif len(result.machines) > 1:
            print("Cannot start multiple machines at once")
            print("Be more specific with your machine query")
        else:
            print(f"Could not find machine to start: {args.start}")
    elif args.info:
        try:
            machine = client.info()
        except StopIteration:
            print("The machine is currently busy with another operation")
        else:
            if machine is not None:
                print(f"Machine Name: {machine.machine.name}")
                print(f"Machine ID:   {machine.machine.id}")
                print(f"Machine IP:   {machine.ip}")
            else:
                print("No active machine available")
    elif args.kill:
        try:
            machine = client.stop()
        except StopIteration:
            print("The machine is currently busy with another operation")
        else:
            if machine is not None:
                start_time = time.perf_counter()
                print(f"Stopped: {machine}")
                print("The machine takes time to stop completely")
                print("Please wait...")
                total = 60
                address = None
                for second in range(total):
                    time.sleep(1)
                    address = client.target()
                    if address is None:
                        end_time = time.perf_counter()
                        elapsed = round(end_time - start_time, 2)
                        print(f"Elapsed time: {elapsed} seconds")
                        print(f"Finished: {machine} was stopped")
                        break
                else:
                    print(f"There was a problem stopping: {machine}")
            else:
                print("No active machine available to stop")
    elif args.reset:
        try:
            machine = client.reset()
        except StopIteration:
            print("The machine is currently busy with another operation")
        else:
            if machine is not None:
                start_time = time.perf_counter()
                print(f"Resetting: {machine}")
                print("The machine takes time to start up completely")
                print("Please wait...")
                total = 300
                address = None
                for second in range(total):
                    time.sleep(1)
                    try:
                        address = client.target()
                    except StopIteration:
                        pass
                    else:
                        if address is not None:
                            end_time = time.perf_counter()
                            elapsed = round(end_time - start_time, 2)
                            print(f"Elapsed time: {elapsed} seconds")
                            print(f"Finished: {address}")
                            break
                else:
                    print(f"There was a problem resetting: {machine}")
            else:
                print("No active machine available to reset")
    elif args.flag:
        flag_parts = args.flag.split(":")
        if len(flag_parts) == 2:
            flag, difficulty = flag_parts
            try:
                difficulty = int(difficulty)
            except ValueError:
                print("Invalid difficulty argument, must be an integer")
            else:
                if difficulty % 10:
                    print("Difficulty must be a multiple of 10")
                elif difficulty < 10 or difficulty > 100:
                    print("Difficulty must be between 10 and 100")
                else:
                    result = client.submit(flag, difficulty)
                    if result is not None:
                        machine, message = result
                        print(f"Submitted flag for: {machine}")
                        print(f"Flag {flag} -> Difficulty {difficulty}")
                        print(f"Message: {message}")
                    else:
                        print("No active machine available to submit flag for")
        else:
            print(f"Invalid flag format: {args.flag}")
            print("Correct format is <flag>:<difficulty>")
    elif args.local:
        address = client.get_local_ip()
        if address is not None:
            print(address)
        else:
            print("Interface tun0 is not up, connect to VPN first")
    elif args.target:
        try:
            address = client.target()
        except StopIteration:
            print("The machine is currently busy with another operation")
        else:
            if address is not None:
                print(address)
            else:
                print("No active machine available to check target IP for")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--api-token-path",
        dest="token_path",
        required=False, type=str,
        default="/etc/hackthebox/api-token.txt",
        help="specify path to the HackTheBox app token file path"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-q", "--query",
        dest="query", type=str,
        help="specify machine name to query for"
    )
    group.add_argument(
        "-s", "--start",
        dest="start", type=str,
        help="specify machine name to start/spawn"
    )
    group.add_argument(
        "-i", "--info",
        action="store_true",
        help="specify info flag to get active machine info"
    )
    group.add_argument(
        "-k", "--kill",
        action="store_true",
        help="specify kill flag to stop an active machine"
    )
    group.add_argument(
        "-r", "--reset",
        action="store_true",
        help="specify reset flag to reset an active machine"
    )
    group.add_argument(
        "-f", "--flag",
        dest="flag", type=str,
        help="specify flag to submit flag and difficulty to active machine"
    )
    group.add_argument(
        "-l", "--local",
        action="store_true",
        help="specify local flag to get local tun0 IP address"
    )
    group.add_argument(
        "-t", "--target",
        action="store_true",
        help="specify target flag to get the IP address of an active machine"
    )
    args = parser.parse_args()
    main(args)
