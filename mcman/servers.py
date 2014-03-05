""" mcman servers module. """

import spacegdn
from mcman.utils import list_names, download


class Servers(object):

    """ The servers command for mcman. """

    def __init__(self, args):
        """ Parse commands, and execute tasks. """
        self.args = args

        spacegdn.BASE = args.base_url
        spacegdn.USER_AGENT = args.user_agent

        if args.subcommand is 'servers':
            self.servers()
        elif args.subcommand is 'channels':
            self.channels()
        elif args.subcommand is 'versions':
            self.versions()
        elif args.subcommand is 'builds':
            self.builds()
        elif args.subcommand is 'download':
            self.download()
        elif args.subcommand is 'identify':
            self.identify()
        else:
            return

    def servers(self):
        """ List servers. """
        print('Fetching server list from SpaceGDN...')

        result = spacegdn.jars()

        if type(result) is list:
            print('Available jars:')
            names = [jar['name'] for jar in result]
            if len(names) > 0:
                print('   ', list_names(names))
            else:
                print('    No results...')
        else:
            print('Recieved an error from SpaceGDN:')
            print('   ', result['message'])

    def channels(self):
        """ List channels. """
        print('Fetching channel list from SpaceGDN...')

        server = spacegdn.get_id(jar=self.args.server)
        result = spacegdn.channels(jar=server)

        if type(result) is list:
            print('Available channels for {}:'.format(self.args.server))

            names = [channel['name'] for channel in result]
            if len(names) > 0:
                print('   ', list_names(names))
            else:
                print('    No results...')
        else:
            print('Recieved an error from SpaceGDN:')
            print('   ', result['message'])

    def versions(self):
        """ List versions. """
        print('Fetching version list from SpaceGDN...')

        server = spacegdn.get_id(jar=self.args.server)
        channel = None
        if self.args.channel is not None:
            channel = spacegdn.get_id(jar=server, channel=self.args.channel)
        result = spacegdn.versions(jar=server, channel=channel)

        if type(result) is list:
            print('Available versions for {}:'.format(self.args.server))
            # Sort and limit the results
            names = list(reversed(sorted(
                [version['version'] for version in result])))
            if self.args.size >= 0:
                names = names[
                    :min(self.args.size, len(names))]
            else:
                names = names[
                    max(self.args.size, -len(names)):]

            if len(names) > 0:
                print('   ', list_names(names))
            else:
                print('    No results...')
        else:
            print('Recieved an error from SpaceGDN:')
            print('   ', result['message'])

    def builds(self):
        """ List builds. """
        print('Fetching build list from SpaceGDN...')

        server = spacegdn.get_id(jar=self.args.server)
        channel = None
        if self.args.channel is not None:
            channel = spacegdn.get_id(jar=server, channel=self.args.channel)
        version = None
        if self.args.version is not None:
            version = spacegdn.get_id(jar=server, channel=self.args.channel,
                                      version=self.args.version)
        result = spacegdn.builds(jar=server, channel=channel,
                                 version=version)

        if type(result) is list:
            print('Available builds for {}:'.format(self.args.server))
            # Sort and limit the results
            names = list(reversed(sorted(
                [build['build'] for build in result])))
            if self.args.size >= 0:
                names = names[
                    :min(self.args.size, len(names))]
            else:
                names = names[
                    max(self.args.size, -len(names)):]

            if len(names) > 0:
                print('   ', list_names(names))
            else:
                print('    No results...')
        else:
            print('Recieved an error from SpaceGDN:')
            print('   ', result['message'])

    def download(self):
        """ Download a server. """
        print('Finding build...')
        server = spacegdn.get_id(jar=self.args.server)
        channel = None
        if self.args.channel is not None:
            channel = spacegdn.get_id(jar=server, channel=self.args.channel)
        version = None
        if self.args.version is not None:
            version = spacegdn.get_id(jar=server, channel=self.args.channel,
                                      version=self.args.version)
        build = None
        if self.args.build is not None:
            build = spacegdn.get_id(jar=server, channel=self.args.channel,
                                    version=self.args.version,
                                    build=self.args.build)
        result = spacegdn.builds(jar=server, channel=channel,
                                 version=version, build=build)
        if type(result) is list:
            if len(result) < 1:
                print('No results...')
                return
            result.sort(key=lambda build: build['build'], reverse=True)
            build = result[0]
            # We don't check if we got a successfull result because the id's
            # were supplied by SpaceGDN
            channel = spacegdn.channels(channel=build['channel_id'])[0]['name']
            version = spacegdn.versions(
                version=build['version_id'])[0]['version']
            print('Found build: channel: {}, version: {}, build: {}'
                  .format(channel, version, build['build']))
            print('Press enter to download, Ctrl+C or Ctrl+D to abort')
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                return
            download(build['url'], file_name=self.args.output,
                     checksum=build['checksum'])
        else:
            print('Recieved an error from SpaceGDN:')
            print('   ', result['message'])

    def identify(self):
        """ Identify what server a jar is. """
        print('The SpaceGDN currently have no way to search.')