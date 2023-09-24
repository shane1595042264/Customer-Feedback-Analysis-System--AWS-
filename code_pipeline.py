from aws_cdk import (
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    core
)

class MyCICDPipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        pipeline = codepipeline.Pipeline(
            self, 'MyPipeline',
            artifact_bucket=s3.Bucket(self, 'PipelineBucket')
        )

        source_action = codepipeline_actions.GitHubSourceAction(
            action_name='GitHub_Source',
            owner='GITHUB_OWNER',
            repo='GITHUB_REPO',
            oauth_token=core.SecretValue.secrets_manager('GITHUB_TOKEN_NAME'),
            output=source_output,
            branch='main'
        )

        build_action = codepipeline_actions.CodeBuildAction(
            action_name='CodeBuild',
            project=codebuild.Project(
                self, 'MyProject',
                source=codebuild.Source.git_hub(
                    owner='GITHUB_OWNER',
                    repo='GITHUB_REPO'
                )
            ),
            input=source_output,
            outputs=[build_output]
        )

        pipeline.add_stage(
            stage_name='Source',
            actions=[source_action]
        )

        pipeline.add_stage(
            stage_name='Build',
            actions=[build_action]
        )
