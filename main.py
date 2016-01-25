import sys

import vindinium


def main():
    if len(sys.argv) < 3:
        print("Usage: %s <key> <[training|competition]> [gameId]" % (sys.argv[0]))
        print('Example: %s mySecretKey competition myGameId' % (sys.argv[0]))
        print('Example: %s mySecretKey training' % (sys.argv[0]))
    else:
        key = sys.argv[1]
        mode = sys.argv[2]

        if mode != "training" and mode != "competition":
            print("Invalid game mode. Please use 'training' or 'competition'.")
        else:
            client = vindinium.Client(
                    server='http://vindinium.org',
                    key=key,
                    mode=mode,
                    n_turns=300,
                    open_browser=True
            )
            url = client.run(vindinium.bots.RusselBot())
            print 'Replay in:', url
        print("\nGame finished!")




if __name__ == '__main__':
    main()
