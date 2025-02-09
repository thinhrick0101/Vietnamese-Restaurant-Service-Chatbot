from brain_agent import BrainAgent
import runpod

def main():
    agent_controller = BrainAgent()
    runpod.serverless.start({"handler": agent_controller.get_response})


if __name__ == "__main__":
    main()